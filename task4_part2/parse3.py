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
    try:
        required_bunch_name = bunch.get(KEY_REQUIRE)

        if required_bunch_name:
            list_of_dependencies.append(bunch_name)
            for key in required_bunch_name:
                if key not in list_of_dependencies:
                    list_of_dependencies.append(key)
                print('list1', str(list_of_dependencies))
    except (AttributeError, KeyError, TypeError):


        print('list2', str(list_of_dependencies))
    return list_of_dependencies


def reverse_dependencies(dependencies):
    list_of_reversed_dependencies = []
    for key in reversed(dependencies):
        list_of_reversed_dependencies.append(key)
    return list_of_reversed_dependencies

if __name__ == "__main__":
    configfile = get_config(configpath)
    create_dependencies = resolve_dependencies(configfile, key_name)
    print(create_dependencies)
    delete_dependencies = reverse_dependencies(create_dependencies)
    print(delete_dependencies)
