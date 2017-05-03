top = {"<Part: 1.1>": {"<Part: 1.1.1>": {"<Part: 1.1.1.1>": {}}, "<Part: 1.1.2>": {}}, "<Part: 1.2>": {"<Part: 1.2.1>": {}, "<Part: 1.2.2>": {}}, "<Part: 1.3>": {}}

def grab_children(father):
    local_list = []
    for key, value in father.items():
        local_list.append(key)
        local_list.extend(grab_children(value))
    return local_list

print(grab_children(top))
