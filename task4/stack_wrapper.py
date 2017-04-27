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
    except (OSError, IOError) as error:
        print("I/O Error: {error_message}".format(error_message=error))
        exit(1)
    except (BotoCoreError, ClientError) as error:
        print("Validate Error: {error_message}".format(error_message=error))
        exit(1)
    else:
        print("Template \"{file}\" is valid".format(file=file_name))
        template_opened.close()
        return read_template


# existing stack function
def stack_exists(stackname):
    """Check if stack exists"""
    try:
        stack_exists = client.describe_stacks(
            StackName=stackname
        )
    except (BotoCoreError, ClientError) as error:
        print("Existing Error: {error_message}".format(error_message=error))
        exit(1)
    else:
        print("Stack \"{stack}\" exists".format(stack=stackname))


# create waiter function
def set_waiter(stackname, waiter_type):
    try:
        # add waiter
        waiter = client.get_waiter(waiter_type)

        # wait until stack would be updated
        waiter.wait(StackName=stackname)
    except (WaiterError, WaiterConfigError) as error:
        print("Waiter Error: {error_message}".format(error_message=error))
        exit(1)
    else:
        print("Stack \"{stack}\" get status:  {status}".format(stack=stackname, status=waiter_type))


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
        print(created_stack)
    except (BotoCoreError, ClientError) as error:
        print("Update Error: {error_message}".format(error_message=error))
        exit(1)

    # set waiter
    set_waiter(args.stack_name, 'stack_create_complete')


# update stack function
def update_stack(args):
    """Updates aws cloudformation stack from file"""

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
        print(updated_stack)
    except (BotoCoreError, ClientError) as error:
        print("Update Error: {error_message}".format(error_message=error))
        exit(1)

    # set waiter
    set_waiter(args.stack_name, 'stack_update_complete')


# delete stack function
def delete_stack(args):
    """Deletes aws cloudformation stack"""
    # check if stack exists
    stack_exists(args.stack_name)

    # try delete stack
    try:
        deleted_stack = client.delete_stack(
            StackName=args.stack_name,
        )
        print(deleted_stack)
    except (BotoCoreError, ClientError) as error:
        print("Update Error: {error_message}".format(error_message=error))
        exit(1)
    # set waiter
    set_waiter(args.stack_name, 'stack_delete_complete')


def main():
    """ entry point """
    args = get_args()
    args.func(args)


if __name__ == '__main__':
    main()
