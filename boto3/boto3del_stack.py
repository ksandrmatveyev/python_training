#! /usr/bin/env python
# import boto3 library
import boto3
from sys import exit
from botocore.exceptions import BotoCoreError, ClientError, WaiterError, WaiterConfigError

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
    try:
        # delete stack
        deleted_stack = client.delete_stack(
            StackName=stackname,
        )

        # add waiter
        waiter = client.get_waiter('stack_delete_complete')

        # wait until stack would be created
        waiter.wait(StackName=stackname)
        print(deleted_stack)
    except ClientError as error:
        print("Client Error: {error_message}".format(error_message=error))
        exit(1)
    except (WaiterError, WaiterConfigError) as error:
        print("Waiter Error: {error_message}".format(error_message=error))
        exit(1)

if __name__ == '__main__':
    delete_stack()
