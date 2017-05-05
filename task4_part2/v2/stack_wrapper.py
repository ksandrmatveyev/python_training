#! /usr/bin/env python
from sys import exit, argv
import logging
import argparse
from operator import itemgetter
import yaml
import boto3
from botocore.exceptions import BotoCoreError, ClientError, WaiterConfigError, WaiterError


# for loging configuration
LOGFORMAT = '%(asctime)s | %(levelname)s | %(funcName)s | %(message)s'
DATEFORMAT = '%m/%d/%Y %I:%M:%S %p'

# for boto3 stack functions
ACTION_CREATE = 'create'
ACTION_UPDATE = 'update'
ACTION_DELETE = 'delete'

# types for setting waiters in waiter function
WAITERS = {
    ACTION_CREATE: 'stack_create_complete',
    ACTION_UPDATE: 'stack_update_complete',
    ACTION_DELETE: 'stack_delete_complete',
}
logger = logging.getLogger(__name__)
client = boto3.client('cloudformation')

# config file keys
KEY_REQUIRE = "require"


def get_args():
    """Parsing CLI commands using argparse with subparsers for common stack functions.
    Dublication of log and logfile arguments, because subparsers are using
    """

    parser = argparse.ArgumentParser(description='AWS stack wrapper')
    subparsers = parser.add_subparsers()

    # Create stack parser
    parser_create = subparsers.add_parser('create-stack', help='create new stack from file')
    parser_create.add_argument('stack_name', help='set stack name')
    parser_create.add_argument('--config',
                               required=False,
                               default='config.yaml',
                               help='set path to config file')
    parser_create.add_argument('--log',
                               type=str,
                               default='INFO',
                               choices=['INFO', 'DEBUG', 'ERROR'],
                               required=False,
                               help='which log level. DEBUG, INFO, ERROR')
    parser_create.add_argument('--logfile',
                               required=False,
                               default=None,
                               help='write log to file')
    parser_create.set_defaults(func=create_stack)

    # Update stack parser
    parser_update = subparsers.add_parser('update-stack', help='update existing stack from file')
    parser_update.add_argument('stack_name', help='set stack name')
    parser_update.add_argument('--config',
                               required=False,
                               default='config.yaml',
                               help='set path to config file')
    parser_update.add_argument('--log',
                               type=str,
                               default='INFO',
                               choices=['INFO', 'DEBUG', 'ERROR'],
                               required=False,
                               help='which log level. DEBUG, INFO, ERROR')
    parser_update.add_argument('--logfile',
                               required=False,
                               default=None,
                               help='write log to file')
    parser_update.set_defaults(func=update_stack)

    # Delete stack parser
    parser_delete = subparsers.add_parser('delete-stack', help='delete existing stack')
    parser_delete.add_argument('stack_name', help='set stack name')
    parser_delete.add_argument('--config',
                               required=False,
                               default='config.yaml',
                               help='set path to config file')
    parser_delete.add_argument('--log',
                               type=str,
                               default='INFO',
                               choices=['INFO', 'DEBUG', 'ERROR'],
                               required=False,
                               help='which log level. DEBUG, INFO, ERROR')
    parser_delete.add_argument('--logfile',
                               required=False,
                               default=None,
                               help='write log to file')
    parser_delete.set_defaults(func=delete_stack)
    # if no arguments, show help
    if len(argv) == 1:
        parser.print_help()
        exit(1)
    return parser.parse_args()


def open_file(file_path):
    """try to open and read cloudformation template file"""

    try:
        # open template file
        template_opened = open(file_path)
        # read template file
        read_template = template_opened.read()

    except (OSError, IOError) as error:
        logger.error("I/O Error: {error_message}".format(error_message=error))
        exit(1)
    else:
        logger.info("Template \"{file}\" was read".format(file=file_path))
        template_opened.close()
        return read_template


# def validate_template(read_template):
#     """validate cloudformation template file, which was read previously"""
#
#     validate_template = client.validate_template(
#         TemplateBody=read_template,
#     )


def get_template_params(read_template):
    """return parameters from template file, which was read previously.
    Parameters are being written  into list as key-value pairs.
    If no DefaultValue for parameter, set None (using get())
    """

    valid_template = client.validate_template(
        TemplateBody=read_template
    )
    logger.info("Template is valid")
    template_params = valid_template.get('Parameters')
    list_of_parameters = []
    for oldkey in template_params:
        parameter = {
            "ParameterKey": oldkey["ParameterKey"],
            "ParameterValue": oldkey.get('DefaultValue')
        }
        list_of_parameters.append(parameter)
    list_of_parameters = sorted(list_of_parameters,
                                key=itemgetter('ParameterKey',
                                               'ParameterValue'))

    logger.debug("Template has parameters: {params}".format(params=list_of_parameters))
    logger.info('Template parameters were parsed')
    return list_of_parameters


def get_config(config_path):
    """try open and read yaml config file.
    Return read config, if no exception
    """

    try:
        with open(config_path, 'r') as file_descriptor:
            read_config = yaml.load(file_descriptor)
    except (OSError, IOError, yaml.YAMLError) as error:
        logger.error("Config file Error: {error_message}".format(error_message=error))
        exit(1)
    else:
        logger.info("Config file \"{file}\" is valid".format(file=config_path))
        return read_config


def match_parameters(stack_key, template_read, read_config):
    """Matching parameters between template and config.
    Value always is got from config file (default value is ignored)
    """

    try:
        template_params = get_template_params(template_read)
        parameters_key = 'parameters'
        parameters_from_config = read_config.get(stack_key).get(parameters_key)
        resolved_parameters = []
        for item in template_params:
            if item["ParameterKey"] in parameters_from_config:
                value = parameters_from_config[item["ParameterKey"]]
                parameter = {
                    "ParameterKey": item["ParameterKey"],
                    "ParameterValue": value
                }
                resolved_parameters.append(parameter)
    except KeyError as error:
        logger.error("Key \"{key}\" not found in config file".format(key=error))
        exit(1)
    else:
        logger.debug('Matched parameters: {params}'.format(params=resolved_parameters))
        logger.info('Parameters were matched successfully')
        return resolved_parameters


def stack_exists(stack_name):
    """Check if stack exists"""
    try:
        stack_exists = client.describe_stacks(
            StackName=stack_name
        )
    except (BotoCoreError, ClientError):
        logger.info("Stack \"{stack}\" doesn't exist".format(stack=stack_name))
        return False
    else:
        logger.info("Stack \"{stack}\" already exists".format(stack=stack_name))
        return True


def set_waiter(stack_name, waiter_type):
    """set waiter for boto3 operations"""

    try:
        # add waiter
        waiter = client.get_waiter(WAITERS[waiter_type])
        # wait until stack would be updated
        waiter.wait(StackName=stack_name)
    except KeyError as error:
        logger.error("Key Error: {error_message}".format(error_message=error))
        exit(1)
    except (WaiterError, WaiterConfigError) as error:
        logger.error("Waiter Error: {error_message}".format(error_message=error))
        exit(1)
    else:
        logger.info("{operation} stack \"{stack}\": {status}".format(operation=waiter_type,
                                                                     stack=stack_name,
                                                                     status=WAITERS[waiter_type]))


def get_dict_of_lists_dependency(read_config):
    """return dictionary of lists as value for each key in config file"""

    dict_dependency = {key: [] for key in read_config.keys()}
    for key, nested_values in read_config.items():
        required_key_name = nested_values.get(KEY_REQUIRE)
        if required_key_name:
            dict_dependency[required_key_name].append(key)
    logger.debug('All dependencies: {dict}'.format(dict=dict_dependency))
    return dict_dependency


def resolve_create_dependencies(read_config, stack_key):
    """return list of stack dependencies chain for creating of assigned stack"""

    list_of_dependencies = [stack_key]
    required_key_name = read_config[stack_key].get(KEY_REQUIRE)
    if required_key_name:
        list_of_dependencies = resolve_create_dependencies(read_config, required_key_name) + list_of_dependencies
    logger.debug('List dependency for creating of stack \"{stack}\": {list_create}'.format(
                                                                                    list_create=list_of_dependencies,
                                                                                    stack=stack_key))
    return list_of_dependencies


def resolve_delete_dependencies(dict_dependency, stack_key):
    """return list of stack dependencies chain for deleting of assigned stack"""

    list_of_dependencies = [stack_key]
    for dependency in dict_dependency[stack_key]:
        list_of_dependencies = resolve_delete_dependencies(dict_dependency, dependency) + list_of_dependencies
    logger.debug('List dependency for deleting of stack \"{stack}\": {list_create}'.format(
                                                                                    list_create=list_of_dependencies,
                                                                                    stack=stack_key))
    return list_of_dependencies


def create_stack(args):
    """Reads and validates cloudformation template file,
    Then creates aws cloudformation stack from this template.
    Finally, set waiter using function with constant action
    """

    configfile = get_config(args.config)
    list_create_dependency = resolve_create_dependencies(configfile, args.stack_name)
    for stack_key in list_create_dependency:
        template_path = configfile[stack_key].get('template')
        read_template = open_file(template_path)
        params = match_parameters(stack_key, read_template, configfile)
        if stack_exists(stack_key):
            continue
        created_stack = client.create_stack(
            StackName=stack_key,
            TemplateBody=read_template,
            Parameters=params,
            Capabilities=[
                'CAPABILITY_IAM',
                'CAPABILITY_NAMED_IAM',
            ]
        )
        logger.debug("Create stack request: {request}".format(request=created_stack))
        set_waiter(stack_key, ACTION_CREATE)


def update_stack(args):
    """Reads and validates cloudformation template file,
    then updates aws cloudformation stack from this template.
    Finally, set waiter using function with constant action
    """

    configfile = get_config(args.config)
    list_update_dependency = resolve_create_dependencies(configfile, args.stack_name)
    for stack_key in list_update_dependency:
        template_path = configfile[stack_key].get('template')
        read_template = open_file(template_path)
        params = match_parameters(stack_key, read_template, configfile)
        if stack_exists(stack_key):
            updated_stack = client.update_stack(
                StackName=stack_key,
                TemplateBody=read_template,
                Parameters=params,
                Capabilities=[
                    'CAPABILITY_IAM',
                    'CAPABILITY_NAMED_IAM',
                ]
            )
            logger.debug("Update stack request: {request}".format(request=updated_stack))
            set_waiter(stack_key, ACTION_UPDATE)


def delete_stack(args):
    """Checks if aws cloudformation stack exists,
    then deletes this stack.
    Finally, set waiter using function with constant action
    """

    configfile = get_config(args.config)
    full_list_dependecies = get_dict_of_lists_dependency(configfile)
    list_delete_dependency = resolve_delete_dependencies(full_list_dependecies, args.stack_name)
    for stack_key in list_delete_dependency:
        if stack_exists(stack_key):
            deleted_stack = client.delete_stack(
                StackName=stack_key,
            )
            logger.debug("Delete stack request: {request}".format(request=deleted_stack))
            set_waiter(stack_key, ACTION_DELETE)


def main():
    """ entry point: getting arguments,
    handling log level argument for logging config,
    configuring logging config and
    handling exceptions of functions, which used those arguments    
    """

    args = get_args()
    loglevel = args.log
    numeric_level = getattr(logging, loglevel.upper(), None)
    logging.basicConfig(filename=args.logfile,
                        level=numeric_level,
                        format=LOGFORMAT,
                        datefmt=DATEFORMAT)
    try:
        args.func(args)
    except (BotoCoreError, ClientError) as error:
        logger.error("Error: {error_message}".format(error_message=error))
        exit(1)

if __name__ == '__main__':
    main()
