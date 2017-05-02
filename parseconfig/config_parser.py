import yaml

with open("config.yaml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

for section in cfg:
    print(section)
print(cfg['mysql'])
print(cfg['other'])
items = cfg.get('other')
print(items)
for key, value in items.items():
    print(key, value)