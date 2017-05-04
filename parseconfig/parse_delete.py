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

new_dict = {}


def get_list_dependency(config, stack_key):
    nested_values = config[stack_key]
    print('nested of:', nested_values)
    required_key_name = nested_values.get(KEY_REQUIRE)
    print('required key name:', required_key_name)
    new_dict[stack_key] = required_key_name
    return new_dict

list = []


def get_list_of_dict_dependency(config, stack_key):
    nested_values = config[stack_key]
    # print('nested of:', key_name,  nested_values)
    required_key_name = nested_values.get(KEY_REQUIRE)
    # print('required key name:', required_key_name)
    parameter = {
        stack_key: required_key_name
    }
    list.append(parameter)
    return list


list2 = []


def get_list_of_dict_dependency2(config):
    for key in config:
        nested_values = config[key]
        required_key_name = nested_values.get(KEY_REQUIRE)
        if required_key_name is not None:
            parameter = {
                required_key_name: key
            }
        else:
            parameter = {
                key: required_key_name
            }
        list2.append(parameter)
    return list2

list3 = []
# dictn = {}


def get_dict_of_lists_dependency(config):
    dictn = {}
    for key in config:
        nested_values = config[key]
        required_key_name = nested_values.get(KEY_REQUIRE)
        if required_key_name is not None:
            dictn.setdefault(required_key_name, []).append(key)
        else:
            dictn.setdefault(key, []).append(required_key_name)
    return dictn


if __name__ == "__main__":
    configfile = get_config(configpath)
    print(configfile)
    # list_dependency = get_list__dependency(configfile, stack)
    # print(list_dependency)
    # list_of_dict_dependency = get_list_of_dict_dependency(configfile, stack)
    # print(list_of_dict_dependency)
    # list_of_dict_dependency2 = get_list_of_dict_dependency2(configfile)
    # print(list_of_dict_dependency2)
    list_of_dict_dependency3 = get_dict_of_lists_dependency(configfile)
    print(list_of_dict_dependency3)
