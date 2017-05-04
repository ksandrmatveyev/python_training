import yaml

def get_config(configpath):
    """return all data from yaml config file"""
    try:
        with open(configpath, 'r') as file_descriptor:
            data = yaml.load(file_descriptor)
    except (OSError, IOError, yaml.YAMLError) as error:
        print("Config file Error: {error_message}".format(error_message=error))
        exit(1)
    else:
        return data

print(get_config('config.yaml'))
