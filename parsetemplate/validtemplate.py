#! /usr/bin/env python
import boto3

client = boto3.client('cloudformation')
templ_open = open('WebApp.json')
templ_opened = templ_open.read()
templ_valid = client.validate_template(
    TemplateBody=templ_opened
)
print(templ_valid['Parameters'])
templ_open.close()
