#! /usr/bin/env python
import boto3
import yaml
from collections import namedtuple

configpath = 'config.yaml'
KEY_REQUIRE = "require"


def get_config(configpath):
    with open(configpath, 'r') as file_descriptor:
        data = yaml.load(file_descriptor)
    return data

def get_dict_of_lists_dependency(config):
    dict_dependency = {key: [] for key in config.keys()}
    for key, nested_values in config.items():
        required_key_name = nested_values.get(KEY_REQUIRE)
        if required_key_name:
            dict_dependency[required_key_name].append(key)
    return dict_dependency

def resolve_dependencies(config, stack_key):
    list_of_dependencies = [stack_key]
    required_key_name = config[stack_key].get(KEY_REQUIRE)
    if required_key_name:
        list_of_dependencies = resolve_dependencies(config, required_key_name) + list_of_dependencies
    return list_of_dependencies

def resolve_upto(dependencies, stack_key):
    list_of_dependencies = [stack_key]
    for dependency in dependencies[stack_key]:
        list_of_dependencies = resolve_upto(dependencies, dependency) + list_of_dependencies
    return list_of_dependencies

if __name__ == "__main__":
    configfile = get_config(configpath)
    # print(configfile)
    stack = 'NetworkStack'
    print(configfile[stack].get('name'))
    print(configfile[stack].get('template'))
    dict_dependency = get_dict_of_lists_dependency(configfile)
    print(resolve_upto(dict_dependency, stack))
    create_list_order = resolve_dependencies(configfile, stack)
    print(create_list_order)
