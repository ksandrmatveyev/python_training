#! /usr/bin/env python
# import boto3 library
import boto3
import json

def create_stack():
    # read template file
    with open('SampleNetworkCrossStack.json') as json_data:
        template = json.load(json_data)

    # add cf client
    client = boto3.client('cloudformation')

    # create stack
    stack = client.create_stack(
        StackName='TestStack',
        TemplateBody=template,
        Capabilities=[
            'CAPABILITY_IAM'|'CAPABILITY_NAMED_IAM',
        ]
    )

    # add waiter
    waiter = client.get_waiter('stack_create_complete')

    # wait until stack would be created
    waiter.wait(StackName='TestStack')

create_stack()
