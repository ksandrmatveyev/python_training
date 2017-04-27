#! /usr/bin/env python
# import boto3 library
import boto3
from sys import exit
from botocore.exceptions import BotoCoreError, ClientError, WaiterError, WaiterConfigError

template_file = 'SampleNetworkCrossStack.json'
stackname = 'TestStack'
# add cf client
client = boto3.client('cloudformation')


# try open and read a file
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


def create_stack():
    """Creates aws cloudformation stack from file"""
    # get read template
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
    except ClientError:
        try:
            # create stack
            created_stack = client.create_stack(
                StackName=stackname,
                TemplateBody=read_template,
                Capabilities=[
                    'CAPABILITY_IAM',
                    'CAPABILITY_NAMED_IAM',
                ]
            )

            # add waiter
            waiter = client.get_waiter('stack_create_complete')

            # wait until stack would be created
            waiter.wait(StackName=stackname)
            print(created_stack)
        except (ClientError, BotoCoreError, WaiterError, WaiterConfigError) as error:
            print("Create Error: {error_message}".format(error_message=error))
            exit(1)
    except BotoCoreError as core_except:
        print("Core Error: {}".format(core_except))
        exit(1)
    else:
        print("Error: Stack \"{}\" already exists".format(args.stack_name))
        exit(1)

if __name__ == '__main__':
    create_stack()
