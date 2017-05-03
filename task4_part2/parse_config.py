#! /usr/bin/env python
import boto3
import yaml
from collections import namedtuple

configpath = 'test.yaml'
key_name = 'App1'
KEY_REQUIRE = "require"


def get_config(configpath):
    with open(configpath, 'r') as file_descriptor:
        data = yaml.load(file_descriptor)
    return data

list_of_dependencies = []


def resolve_dependencies(config, key_name):
    key_value = config[key_name]
    # print('bunch:', key_value)
    try:
        required_key_name = key_value.get(KEY_REQUIRE)
        # print('required key name:', required_key_name)
        if required_key_name:
            list_of_dependencies.append(required_key_name)
        required_value = resolve_dependencies(config, required_key_name)
        # print(required_value)
        # required_value.extend(key_value[1:])
        return required_value
    except (AttributeError, KeyError, TypeError):
        return key_value


if __name__ == "__main__":
    configfile = get_config(configpath)
    create_dependencies = resolve_dependencies(configfile, key_name)
    print(str(list_of_dependencies))
    # print(create_dependencies)
