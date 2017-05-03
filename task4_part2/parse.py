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


def resolve_dependencies(config, bunch_name):
    print('bunch_name', bunch_name)
    bunch = config[bunch_name]
    print('bunch', bunch)
    try:
        required_bunch_name = bunch.get(KEY_REQUIRE)
        list_of_dependencies = []
        if required_bunch_name:
            list_of_dependencies.append(bunch_name)
            for key in required_bunch_name:
                list_of_dependencies.append(key)
    except (AttributeError, KeyError, TypeError) as e:
        # print('no dependencies for {bunch}'.format(bunch=bunch_name))
        # pass
        print(e)
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
