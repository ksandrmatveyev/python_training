#! /usr/bin/env python
import boto3
import yaml
from collections import namedtuple

configpath = 'test2.yaml'

def get_config(configpath):
    with open(configpath, 'r') as file_descriptor:
        data = yaml.load(file_descriptor)
    return data

configfile = get_config(configpath)
print(configfile['App1'])

KEY_REQUIRE = "require"

list_of_dependencies = []
def resolve_dependencies(config, bunch_name):
    bunch = config[bunch_name]

    try:
        required_bunch_name = bunch.get(KEY_REQUIRE)
        if required_bunch_name:
            list_of_dependencies.append(bunch_name)
            for key in required_bunch_name:
                list_of_dependencies.append(key)
                required_bunch = resolve_dependencies(config, key)
        else:
            list_of_dependencies.append(bunch_name)
            required_bunch = resolve_dependencies(config, required_bunch_name)
    except (AttributeError, KeyError, TypeError):
        # print('no dependencies for {bunch}'.format(bunch=bunch_name))
        pass
    return list_of_dependencies

def reverse_dependencies(dependencies):
    list_of_reversed_dependencies = []
    for key in reversed(dependencies):
        list_of_reversed_dependencies.append(key)
    return list_of_reversed_dependencies

if __name__ == "__main__":
    delete_dependencies = resolve_dependencies(configfile, "App1")
    print(delete_dependencies)
    create_dependencies = reverse_dependencies(delete_dependencies)
    print(create_dependencies)
