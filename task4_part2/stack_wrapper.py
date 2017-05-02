#! /usr/bin/env python
from sys import exit, argv
import logging
import argparse
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


def get_args():
    """Parsing CLI commands using argparse with subparsers for common stack functions.
    Dublication of log and logfile arguments, because subparsers are using
    """

    parser = argparse.ArgumentParser(description='AWS stack wrapper')
    subparsers = parser.add_subparsers()

    # Create stack parser
    parser_create = subparsers.add_parser('create-stack', help='create new stack from file')
    parser_create.add_argument('stack_name', help='set stack name')
    parser_create.add_argument('file', help='set file path')
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
    parser_update.add_argument('file', help='set file path')
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


def open_file(file_name):
    """try to open and read cloudformation template file"""

    try:
        # open template file
        template_opened = open(file_name)
        # read template file
        read_template = template_opened.read()

    except (OSError, IOError) as error:
        logger.error("I/O Error: {error_message}".format(error_message=error))
        exit(1)
    else:
        logger.info("Template \"{file}\" is valid".format(file=file_name))
        template_opened.close()
        return read_template


def validate_file(read_file):
    """validate cloudformation template file"""
    validate_template = client.validate_template(
        TemplateBody=read_file,
    )


def stack_exists(stackname):
    """Check if stack exists"""

    stack_exists = client.describe_stacks(
        StackName=stackname
    )
    logger.info("Stack \"{stack}\" exists".format(stack=stackname))


def set_waiter(stackname, waiter_type):
    """set waiter for boto3 operations"""

    try:
        # add waiter
        waiter = client.get_waiter(WAITERS[waiter_type])
        # wait until stack would be updated
        waiter.wait(StackName=stackname)
    except KeyError as error:
        logger.error("Key Error: {error_message}".format(error_message=error))
        exit(1)
    except (WaiterError, WaiterConfigError) as error:
        logger.error("Waiter Error: {error_message}".format(error_message=error))
        exit(1)
    else:
        logger.info("{operation} stack \"{stack}\": {status}".format(operation=waiter_type,
                                                                     stack=stackname,
                                                                     status=WAITERS[waiter_type]))


def create_stack(args):
    """Reads and validates cloudformation template file,
    Then creates aws cloudformation stack from this template.
    Finally, set waiter using function with constant action
    """

    read_template = open_file(args.file)
    validate_file(read_template)
    created_stack = client.create_stack(
        StackName=args.stack_name,
        TemplateBody=read_template,
        Capabilities=[
            'CAPABILITY_IAM',
            'CAPABILITY_NAMED_IAM',
        ]
    )
    logger.debug("Create stack request: {request}".format(request=created_stack))
    set_waiter(args.stack_name, ACTION_CREATE)


def update_stack(args):
    """Reads and validates cloudformation template file,
    then updates aws cloudformation stack from this template.
    Finally, set waiter using function with constant action
    """

    read_template = open_file(args.file)
    validate_file(read_template)
    updated_stack = client.update_stack(
        StackName=args.stack_name,
        TemplateBody=read_template,
        Capabilities=[
            'CAPABILITY_IAM',
            'CAPABILITY_NAMED_IAM',
        ]
    )
    logger.debug("Update stack request: {request}".format(request=updated_stack))
    set_waiter(args.stack_name, ACTION_UPDATE)


def delete_stack(args):
    """Checks if aws cloudformation stack exists,
    then deletes this stack.
    Finally, set waiter using function with constant action
    """

    stack_exists(args.stack_name)
    deleted_stack = client.delete_stack(
        StackName=args.stack_name,
    )
    logger.debug("Delete stack request: {request}".format(request=deleted_stack))
    set_waiter(args.stack_name, ACTION_DELETE)


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
