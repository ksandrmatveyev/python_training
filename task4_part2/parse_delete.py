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


def get_dict_of_lists_dependency(config):
    dict_dependency = {}
    for key in config:
        nested_values = config[key]
        required_key_name = nested_values.get(KEY_REQUIRE)
        if required_key_name is not None:
            dict_dependency.setdefault(required_key_name, []).append(key)
        else:
            dict_dependency.setdefault(key, []).append(required_key_name)
    return dict_dependency


if __name__ == "__main__":
    configfile = get_config(configpath)
    print(configfile)
    dict_of_lists_dependency = get_dict_of_lists_dependency(configfile)
    print(dict_of_lists_dependency)
