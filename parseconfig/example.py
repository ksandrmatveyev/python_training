import yaml

def yaml_loader(filepath):
    """Load a yaml file"""

    with open(filepath, 'r') as file_descriptor:
        data = yaml.load(file_descriptor)
    return data

def yaml_dump(filepath, data):
    """Dumps data to yaml file"""

    with open(filepath, 'w') as file_descriptor:
        yaml.dump(data, file_descriptor)

if __name__ == '__main__':
    filepath = 'config.yaml'
    data = yaml_loader(filepath)
    # print(data)
    items = data.get('mysql')
    for item_name, item_value in items.items():
        print(item_name, item_value)
    items1 = data.get('other')
    for item_name, item_value in items1.items():
        print(item_name, item_value)
