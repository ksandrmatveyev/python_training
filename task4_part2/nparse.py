#! /usr/bin/env python
import boto3
import yaml
from collections import namedtuple

configpath = 'test3.yaml'
key_name = 'App1'
KEY_REQUIRE = "require"


def get_config(configpath):
    with open(configpath, 'r') as file_descriptor:
        data = yaml.load(file_descriptor)
    return data

list1 = []
list2 = []

def resolve_dependencies(config, bunch_name):
    bunch = config[bunch_name]
    print(bunch)
    try:
        required_bunch_name = bunch[KEY_REQUIRE]
        #print(required_bunch_name)
        list2.append(required_bunch_name)
        required_bunch = resolve_dependencies(config, required_bunch_name)
        #print(required_bunch)
        required_bunch.extend(bunch[1:])
        #print(required_bunch)
        return required_bunch
    except (AttributeError, KeyError, TypeError):
        list1.append(bunch['name'])
        return bunch

KEY_NAME = "name"
KEY_PARAMETERS = "parameters"
StackDescription = namedtuple("stack", ["name", "parameters", "file_name"])


# def get_stack_describe(item):
#     try:
#         stack_file_name, nested_parameters = item.popitem()
#         stack_name = nested_parameters.get(KEY_NAME)
#     except AttributeError:
#         stack_file_name = item
#         stack_name = item
#         stack_parameters = {}
#     return StackDescription(name=stack_name,
#                             file_name=stack_file_name,
#                             parameters=stack_parameters)

if __name__ == "__main__":
    config = get_config(configpath)
    plain_config = resolve_dependencies(config, key_name)
    print(plain_config)
    print(list2)
    print(list1)
    # for item in plain_config:
    #     print(get_stack_describe(item))
