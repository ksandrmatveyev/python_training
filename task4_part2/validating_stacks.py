import yaml
import boto3
from botocore.exceptions import BotoCoreError, ClientError, WaiterConfigError, WaiterError


client = boto3.client('cloudformation')






# def stack_exists(stack_name=None):
#     """Check if stack exists"""
#     try:
#         print(stack_name)
#         if stack_name:
#             stack_exists = client.describe_stacks(
#                 StackName=stack_name
#             )
#         if stack_name
#         else:
#             stack_exists = client.describe_stacks()
#     except (BotoCoreError, ClientError):
#         print("Stack \"{stack}\" doesn't exist".format(stack=stack_name))
#     else:
#         print("Stack \"{stack}\" already exists".format(stack=stack_name))
#         return stack_exists
#
# a = stack_exists()
#
# for i in a['Stacks']:
#     print(i.get('StackName'), i.get('StackStatus'), i.get('StackStatusReason'))

client = boto3.client('cloudformation')


def get_config(config_path):
    """try open and read yaml config file.
    Return read config, if no exception
    """

    try:
        with open(config_path, 'r') as file_descriptor:
            read_config = yaml.load(file_descriptor)
    except (OSError, IOError, yaml.YAMLError) as error:
        print("Config file Error: {error_message}".format(error_message=error))
        exit(1)
    else:
        print("Config file \"{file}\" is valid".format(file=config_path))
        return read_config


def validate_stack(config):
    """Checks aws cloudformation stacks status"""
    try:
        configfile = get_config(config)
        stack_list = list(configfile.keys())
        for stack_key in stack_list:
            stack_exists = client.describe_stacks(StackName=stack_key)
            for i in stack_exists['Stacks']:
                print(i.get('StackName')+' has status: '+i.get('StackStatus'))
    except (BotoCoreError, ClientError) as error:
        print("Validate Error: {error_message}".format(error_message=error))


validate_stack('config.yaml')



# def validate_stack(args):
#     """Checks aws cloudformation stacks status"""
#
#     configfile = get_config(args.config)
#     stack_list = list(configfile.keys())
#     for stack_key in stack_list:
#         stack_exists = client.describe_stacks(StackName=stack_key)
#         for i in stack_exists['Stacks']:
#             try:
#                 logger.info("Stack \"{stack}\" has status \"{status}\"".format(stack=i.get('StackName'),
#                                                                                status=i.get('StackStatus')))
#                 logger.debug("Stack \"{stack}\" has status"
#                              " \"{status}\" with reason: {reason}".format(stack=i.get('StackName'),
#                                                                           status=i.get('StackStatus'),
#                                                                           reason=i.get('StackStatusReason')))
#             except (BotoCoreError, ClientError):
#                 logger.error("Stack \"{stack}\" doesn't exist".format(stack=i.get('StackName')))