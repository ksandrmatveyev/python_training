#! /usr/bin/env python
# import boto3 library
import boto3
from sys import exit
from botocore.exceptions import BotoCoreError, ClientError

stackname = 'TestStack'

def delete_stack():
    """Deletes aws cloudformation stack"""

    # add cf client
    client = boto3.client('cloudformation')

    # check if stack exists
    try:
        stack_exists = client.describe_stacks(
            StackName=stackname
        )
    except (BotoCoreError, ClientError) as cf_except:
        print("Error: {}".format(cf_except))
        exit(1)
    else:
        # delete stack
        deleted_stack = client.delete_stack(
            StackName=stackname,
        )

        # add waiter
        waiter = client.get_waiter('stack_delete_complete')

        # wait until stack would be created
        waiter.wait(StackName='TestStack')
        print(deleted_stack)

if __name__ == '__main__':
    delete_stack()
