#!/usr/bin/env python
""" cloudformation example """
import boto3

def main():
    """ entry point """
    file_name = "test.yaml"
    stack_name = "TestStack"
    # open the test file from the current directory
    template = open(file_name).read()
    # create the boto3 cloudformation client
    cloudformation = boto3.client("cloudformation")
    # create the new stack
    cloudformation.create_stack(StackName=stack_name,
                                TemplateBody=template)
    # create the new waiter
    waiter = cloudformation.get_waiter("stack_create_complete")
    # wait until the stack state changes to "CREATE_COMPLETE"
    waiter.wait(StackName=stack_name)

if __name__ == "__main__":
    main()