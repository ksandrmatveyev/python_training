#! /usr/bin/env python
import boto3
import yaml
from collections import namedtuple

configpath = 'test.yaml'
stack = 'App1'
KEY_REQUIRE = "require"


def get_config(configpath):
    with open(configpath, 'r') as file_descriptor:
        data = yaml.load(file_descriptor)
    return data

list_of_dependencies = []


def resolve_dependencies(config, stack_key):
    nested_values = config[stack_key]
    # print('nested of:', key_name,  nested_values)
    required_key_name = nested_values.get(KEY_REQUIRE)
    # print('required key name:', required_key_name)
    if stack_key not in list_of_dependencies:
        list_of_dependencies.append(stack_key)
    if required_key_name:
        list_of_dependencies.append(required_key_name)
        resolve_dependencies(config, required_key_name)
    return list_of_dependencies


if __name__ == "__main__":
    configfile = get_config(configpath)
    print(configfile)

    create_list_order = resolve_dependencies(configfile, stack)
    print(create_list_order)
