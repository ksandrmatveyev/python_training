from collections import namedtuple
import yaml

YAML_CONFIG = """\
base:
  - VPC
  - SecurityGroups
  - IAM
  - S3
nat:
  - require: base
  - NAT
apps:
  - require: nat
  - APPS:
      name: APP1
      args:
        appNumber: '1'
  - APPS:
      name: APP2
      args:
        appNumber: '2'
web:
  - require: apps
  - WEB
"""

KEY_REQUIRE = "require"


def resolve_dependencies(config, bunch_name):
    bunch = config[bunch_name]
    try:
        required_bunch_name = bunch[0][KEY_REQUIRE]
        required_bunch = resolve_dependencies(config, required_bunch_name)
        required_bunch.extend(bunch[1:])
        return required_bunch
    except (AttributeError, KeyError, TypeError):
        return bunch

KEY_NAME = "name"
KEY_PARAMETERS = "args"
StackDescription = namedtuple("stack", ["name", "parameters", "file_name"])

def get_stack_describe(item):
    try:
        stack_file_name, nested_parameters = item.popitem()
        stack_name = nested_parameters.get(KEY_NAME, stack_file_name)
        stack_parameters = nested_parameters.get(KEY_PARAMETERS, {})
    except AttributeError:
        stack_file_name = item
        stack_name = item
        stack_parameters = {}
    return StackDescription(name=stack_name,
                            file_name=stack_file_name,
                            parameters=stack_parameters)

if __name__ == "__main__":
    config = yaml.load(YAML_CONFIG)
    plain_config = resolve_dependencies(config, "web")
    for item in plain_config:
        print(get_stack_describe(item))
