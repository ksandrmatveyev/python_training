from collections import namedtuple
import yaml


def get_config(config_path):
    """try open and read yaml config file.
    Return read config, if no exception
    """

    try:
        with open(config_path, 'r') as file_descriptor:
            config_body = yaml.load(file_descriptor)
    except (OSError, IOError, yaml.YAMLError) as error:
        logger.error("Config file Error: {error_message}".format(error_message=error))
        exit(1)
    else:
        logger.info("Config file \"{file}\" is valid".format(file=config_path))
        return config_body

pin

def convert(dictionary):

    NT = namedtuple('GenericDict', dictionary.keys())
    gen_dict = NT(**dictionary)
    return gen_dict


