#!/usr/bin/env python

import boto3
ec2 = boto3.resource('ec2')

instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

ids = []
for instance in instances:
    print(instance.id, instance.instance_type)
    ids.append(instance.id)

ec2.instances.filter(InstanceIds=ids).stop()
