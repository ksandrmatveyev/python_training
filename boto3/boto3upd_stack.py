#! /usr/bin/env python
# import boto3 library
import boto3
from sys import exit
from botocore.exceptions import BotoCoreError, ClientError, WaiterConfigError, WaiterError

template_file = 'SampleNetworkCrossStack3.json'
stackname = 'TestStack'

def open_file(file_name):
    """open and read file. Check if file exists"""
    try:
        # open template file
        template_opened = open(file_name)
        # read template file
        read_template = template_opened.read()
    except (OSError, IOError) as err:
        print("Error: {}".format(err))
        exit(1)  # or return 0
    else:
        template_opened.close()
        return read_template


def update_stack():
    """Creates aws cloudformation stack from file"""

    # add cf client
    client = boto3.client('cloudformation')
    read_template = open_file(template_file)
    # validate template
    try:
        validate_template = client.validate_template(
            TemplateBody=read_template,
        )
    except (BotoCoreError, ClientError) as val_except:
        print("Error: {}".format(val_except))
        exit(1)

    # check if stack exists
    try:
        stack_exists = client.describe_stacks(
            StackName=stackname
        )
    except (BotoCoreError, ClientError) as core_except:
        print("Core Error: {}".format(core_except))
        exit(1)

    try:
        # update stack
        updated_stack = client.update_stack(
            StackName=stackname,
            TemplateBody=read_template,
            Capabilities=[
                'CAPABILITY_IAM',
                'CAPABILITY_NAMED_IAM',
            ]
        )

        # add waiter
        waiter = client.get_waiter('stack_update_complete')

        # wait until stack would be updated
        waiter.wait(StackName=stackname)
        print(updated_stack)
    except ClientError as error:
        print("Client Error: {error_message}".format(error_message=error))
        exit(1)
    except (WaiterError, WaiterConfigError) as error:
        print("Waiter Error: {error_message}".format(error_message=error))
        exit(1)

if __name__ == '__main__':
    update_stack()
