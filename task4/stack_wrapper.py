#! /usr/bin/env python
from sys import exit
import argparse
import boto3
from botocore.exceptions import BotoCoreError, ClientError, WaiterConfigError, WaiterError


# Configuring argparse
def get_args():
    """Parsing CLI commands"""
    parser = argparse.ArgumentParser(description='AWS stack wrapper')
    subparsers = parser.add_subparsers()

    # Create stack parser
    parser_create = subparsers.add_parser('create-stack', help='create new stack from file')
    parser_create.add_argument('stack_name', help='set stack name')
    parser_create.add_argument('file', help='set file path')
    parser_create.set_defaults(func=create_stack)

    # Update stack parser
    parser_update = subparsers.add_parser('update-stack', help='update existing stack from file')
    parser_update.add_argument('stack_name', help='set stack name')
    parser_update.add_argument('file', help='set file path')
    parser_update.set_defaults(func=update_stack)

    # Delete stack parser
    parser_delete = subparsers.add_parser('delete-stack', help='delete existing stack')
    parser_delete.add_argument('stack_name', help='set stack name')
    parser_delete.set_defaults(func=delete_stack)

    return parser.parse_args()


# add cf client
client = boto3.client('cloudformation')


# try open and read a file
def open_file(file_name):
    """opens, reads and validates a file. Checks if the file exists"""
    try:
        # open template file
        template_opened = open(file_name)

        # read template file
        read_template = template_opened.read()

        # validate template file
        validate_template = client.validate_template(
            TemplateBody=read_template,
        )
    except (OSError, IOError) as err:
        print("I/O Error: {}".format(err))
        exit(1)
    except (BotoCoreError, ClientError) as val_except:
        print("Validate Error: {}".format(val_except))
        exit(1)
    else:
        template_opened.close()
        return read_template


# Create stack function
def create_stack(args):
    """Creates aws cloudformation stack from file"""

    # get read template
    read_template = open_file(args.file)

    # try create stack
    try:
        created_stack = client.create_stack(
            StackName=args.stack_name,
            TemplateBody=read_template,
            Capabilities=[
                'CAPABILITY_IAM',
                'CAPABILITY_NAMED_IAM',
            ]
        )

        # add waiter
        waiter = client.get_waiter('stack_create_complete')

        # wait until stack would be created
        waiter.wait(StackName=args.stack_name)
        print(created_stack)
    except (ClientError, BotoCoreError, WaiterError, WaiterConfigError) as error:
        print("Create Error: {error_message}".format(error_message=error))
        exit(1)


# update stack function
def update_stack(args):
    """Creates aws cloudformation stack from file"""

    # get read template
    read_template = open_file(args.file)

    # try update stack
    try:
        updated_stack = client.update_stack(
            StackName=args.stack_name,
            TemplateBody=read_template,
            Capabilities=[
                'CAPABILITY_IAM',
                'CAPABILITY_NAMED_IAM',
            ]
        )

        # add waiter
        waiter = client.get_waiter('stack_update_complete')

        # wait until stack would be updated
        waiter.wait(StackName=args.stack_name)
        print(updated_stack)
    except (BotoCoreError, ClientError, WaiterError, WaiterConfigError) as error:
        print("Update Error: {error_message}".format(error_message=error))
        exit(1)


# delete stack function
def delete_stack(args):
    """Deletes aws cloudformation stack"""
    # check if stack exists
    try:
        stack_exists = client.describe_stacks(
            StackName=args.stack_name
        )
    except (BotoCoreError, ClientError) as error:
        print("Existing Error: {error_message}".format(error_message=error))
        exit(1)
    else:
        print("Stack \"stack\" exists", stack=args.stack_name)

    # try delete stack
    try:
        deleted_stack = client.delete_stack(
            StackName=args.stack_name,
        )

        # add waiter
        waiter = client.get_waiter('stack_delete_complete')

        # wait until stack would be created
        waiter.wait(StackName=args.stack_name)
        print(deleted_stack)
    except (BotoCoreError, ClientError, WaiterError, WaiterConfigError) as error:
        print("Update Error: {error_message}".format(error_message=error))
        exit(1)


def main():
    """ entry point """
    args = get_args()
    args.func(args)


if __name__ == '__main__':
    main()
