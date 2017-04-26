#! /usr/bin/env python
# import boto3 library
import boto3
from sys import exit

def create_stack():
    """Creates aws cloudformation stack from file"""
    # check if file exists
    try:
        # open template file
        template_path = open('SampleNetworkCrossStack1.json')
    except (OSError, IOError) as err:
        print("Error: {}".format(err))
        exit(1)  # or return 0
    else:
        # read template file
        read_template = template_path.read()
        template_path.close()

    # add cf client
    client = boto3.client('cloudformation')

    # create stack
    stack = client.create_stack(
        StackName='TestStack',
        TemplateBody=read_template,
        Capabilities=[
            'CAPABILITY_IAM',
            'CAPABILITY_NAMED_IAM',
        ]
    )

    # add waiter
    waiter = client.get_waiter('stack_create_complete')

    # wait until stack would be created
    waiter.wait(StackName='TestStack')

if __name__ == '__main__':
    create_stack()
