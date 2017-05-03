#! /usr/bin/env python
import boto3
import yaml
from collections import namedtuple

configpath = 'test.yaml'
key_name = 'App2'
KEY_REQUIRE = "require"


def get_config(configpath):
    with open(configpath, 'r') as file_descriptor:
        data = yaml.load(file_descriptor)
    return data

list_of_dependencies = []


def resolve_dependencies(config, bunch_name):
    bunch = config[bunch_name]
    # print(bunch)
    try:
        required_bunch_name = bunch.get(KEY_REQUIRE)
        # print(required_bunch_name)
        if required_bunch_name:
            list_of_dependencies.append(required_bunch_name)
        else:

            list_of_dependencies.append(bunch_name)
        required_bunch = resolve_dependencies(config, required_bunch_name)
        # print(required_bunch)
        required_bunch.extend(bunch[1:])
        return required_bunch
    except (AttributeError, KeyError, TypeError):
        return bunch


if __name__ == "__main__":
    configfile = get_config(configpath)
    create_dependencies = resolve_dependencies(configfile, key_name)
    print(str(list_of_dependencies))
    print(create_dependencies)
