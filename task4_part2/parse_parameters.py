#! /usr/bin/env python
import boto3
import yaml
from operator import itemgetter

client = boto3.client('cloudformation')
template_path = 'WebAppStack.json'
config_path = 'config.yaml'
stack_key = 'WebAppStack'
parameters_key = 'parameters'


def get_template_params(template):
    template_open = open(template)
    template_read = template_open.read()
    template_valid = client.validate_template(
        TemplateBody=template_read
    )
    template_open.close()
    template_params = template_valid.get('Parameters')
    list_of_parameters = []
    for oldkey in template_params:
        parameter = {
            "ParameterKey": oldkey["ParameterKey"],
            "ParameterValue": oldkey.get('DefaultValue')
        }
        list_of_parameters.append(parameter)
    list_of_parameters = sorted(list_of_parameters,
                                key=itemgetter('ParameterKey',
                                               'ParameterValue'))
    return list_of_parameters


def get_config(configpath):
    with open(configpath, 'r') as file_descriptor:
        data = yaml.load(file_descriptor)
    return data

# template file
# valid_template = get_templ_params(template_path)
# template_params = get_template_params(template_path)
# print(template_params)

# config file
# data = get_config(config_path)
# parameters_from_config = data.get(stack_key).get(parameters_key)

# print(config_params)
# print(parameters_from_config)


# Print different parameters for-loop checking
def match_parameters(template_path, config_path):
    template_params = get_template_params(template_path)
    data = get_config(config_path)
    parameters_from_config = data.get(stack_key).get(parameters_key)

    resolved_parameters = []
    for item in template_params:
        print(item)
        value = None
        if item["ParameterKey"] in parameters_from_config:
            value = parameters_from_config[item["ParameterKey"]]
        elif item["ParameterValue"]:
            value = item["ParameterValue"]
        else:
            print("{key} not found and hasn't default value".format(key=item["ParameterKey"]))
        if value:
            parameter = {
                "ParameterKey": item["ParameterKey"],
                "ParameterValue": value
            }
            resolved_parameters.append(parameter)
    return resolved_parameters

print(match_parameters(template_path, config_path))
#
# def create_stack_with_params(stackname, template, list_params):
#     create_stack = client.create_stack(
#         StackName=stackname,
#         TemplateBody=template,
#         Parameters=config_params,
#         Capabilities=[
#             'CAPABILITY_IAM',
#             'CAPABILITY_NAMED_IAM',
#         ]
#     )
#
# create_stack_with_params('WebApp', template_path,)

