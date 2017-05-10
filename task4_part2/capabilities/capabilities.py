#! /usr/bin/env python
from sys import exit, argv
import logging
import argparse
from operator import itemgetter
from collections import namedtuple
import yaml
import boto3
from botocore.exceptions import BotoCoreError, ClientError, WaiterConfigError, WaiterError

client = boto3.client('cloudformation')


def get_template_params(read_template):
    """return parameters from template file, which was read previously.
    Parameters are being written  into list as key-value pairs.
    If no DefaultValue for parameter, set None (using get())
    """

    valid_template = client.validate_template(
        TemplateBody=read_template
    )
    print("Template is valid")
    template_params = valid_template.get('Parameters')
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

    print("Template has parameters: {params}".format(params=list_of_parameters))
    print('Template parameters were parsed')
    return list_of_parameters


def open_file(file_path):
    """try to open and read cloudformation template file"""

    try:
        # open template file
        template_opened = open(file_path)
        # read template file
        read_template = template_opened.read()

    except (OSError, IOError) as error:
        print("I/O Error: {error_message}".format(error_message=error))
        exit(1)
    else:
        print("Template \"{file}\" was read".format(file=file_path))
        template_opened.close()
        return read_template


def get_template_capabilities(read_template):
    """return capabilities"""

    valid_template = client.validate_template(
        TemplateBody=read_template
    )
    print(valid_template)
    template_capabilities = []
    if valid_template.get('Capabilities'):
        for cap in valid_template.get('Capabilities'):
            template_capabilities.append(cap)
    print(template_capabilities)
    return template_capabilities


templ = open_file('IAMBucketAccess.json')
templ_cap = get_template_capabilities(templ)
templ_params = get_template_params(templ)
print(templ_cap)
print(templ_params)


# def create_stack(stack, template, capabilities):
#     """Reads and validates cloudformation template file,
#     Then creates aws cloudformation stack from this template.
#     Finally, set waiter using function with constant action
#     """
#
#     created_stack = client.create_stack(
#         StackName=stack,
#         TemplateBody=template,
#         Capabilities=capabilities
#     )
#
# create_networkstack = open_file('NetworkStack.json')
# templ_cap1 = get_template_capabilities(create_networkstack)
#
# create_stack('NetworkStack', create_networkstack, templ_cap1)




# def get_template_data(read_template):
#     """return parameters from template file, which was read previously.
#     Parameters are being written  into list as key-value pairs.
#     If no DefaultValue for parameter, set None (using get())
#     """
#
#     valid_template = client.validate_template(
#         TemplateBody=read_template
#     )
#     print("Template is valid")
#     template_dict = {}
#     template_capabilities = valid_template.get('Capabilities')
#     template_dict.setdefault('Capabilities', template_capabilities)
#     template_params = valid_template.get('Parameters')
#     list_of_parameters = []
#     for oldkey in template_params:
#         parameter = {
#             "ParameterKey": oldkey["ParameterKey"],
#             "ParameterValue": oldkey.get('DefaultValue')
#         }
#         list_of_parameters.append(parameter)
#     list_of_parameters = sorted(list_of_parameters,
#                                 key=itemgetter('ParameterKey',
#                                                'ParameterValue'))
#
#     print("Template has parameters: {params}".format(params=list_of_parameters))
#     print('Template parameters were parsed')
#     template_dict.setdefault('Parameters', list_of_parameters)
#     return template_dict
#
#
# templ_data = get_template_data(templ)
# print(templ_data)
