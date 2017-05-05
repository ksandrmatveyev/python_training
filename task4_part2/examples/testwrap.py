import boto3

client = boto3.client('cloudformation')


def validate_template(read_template):
    """validate cloudformation template file, which was read previously"""
    template_opened = open(read_template)
    # read template file
    read_template1 = template_opened.read()
    validate_template = client.validate_template(
        TemplateBody=read_template1,
    )
    return validate_template

a = validate_template('NetworkStack.json')
print(validate_template('NetworkStack.json'))
template_params = a.get('Parameters')
list_of_parameters = []
for oldkey in template_params:
    parameter = {
        "ParameterKey": oldkey["ParameterKey"],
        "ParameterValue": oldkey.get('DefaultValue')
    }
list_of_parameters.append(parameter)
print(list_of_parameters)
