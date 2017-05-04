#! /usr/bin/env python
import boto3
import yaml

template_path = 'WebAppStack.json'
config_path = 'test2.yaml'

def get_templ_param(template):
    client = boto3.client('cloudformation')
    templ_open = open(template)
    templ_opened = templ_open.read()
    templ_valid = client.validate_template(
        TemplateBody=templ_opened
    )
    # print('template\n'
    #       + str(type(templ_valid))
    #       + '\n'
    #       + str(templ_valid))
    # print('template parameters\n'
    #       + str(type(templ_valid['Parameters']))
    #       + '\n'
    #       + str(templ_valid.get('Parameters')))
    templ_open.close()
    return templ_valid


def get_config_param(configpath):
    with open(configpath, 'r') as file_descriptor:
        data = yaml.load(file_descriptor)
    return data


# print('all config\n'
#       + str(type(data))
#       + '\n'
#       + str(data))
# print('config parameters\n'
#       + str(type(data.get('parameters')))
#       + '\n'
#       + str(data.get('parameters')))
# print(str(data.get('parameters')[0]))
# print(str(data.get('parameters')[1]))

# template file
valid_templ = get_templ_param(template_path)
print(valid_templ.get('Parameters'))
templ_param = valid_templ.get('Parameters')

# config file
data = get_config_param(config_path)
print(data.get('App1').get('parameters'))
conf_param = data.get('App1').get('parameters')

# print([x for x in templ_param + conf_param if x not in templ_param or x not in conf_param])
# k1 = templ_param[0].keys()
# v1 = templ_param[0].values()
# k2 = conf_param[0].keys()
# v2 = conf_param[0].values()

# for x in templ_param + conf_param:
#     if x not in templ_param or x not in conf_param:
#         print(x)

for item in templ_param:
    if item not in conf_param:
        print(item)


# pairs = zip(conf_param, templ_param)
# print(any(x != y for x, y in pairs))
# print([(x, y) for x, y in pairs if x != y])


# delete NoEcho and Description keys from valid template responce
# print([{k: v for k, v in d.items() if k != 'NoEcho'} for d in conf_param])


# reassign DefaultValue key to ParameterValue
for oldkey in templ_param:
    oldkey['ParameterValue'] = oldkey['DefaultValue']
    del oldkey['DefaultValue']
    del oldkey['NoEcho']
    del oldkey['Description']
print(str(templ_param))
