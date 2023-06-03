from json import load

def load_json(path):
    with open(path, 'r') as json_file:
        data = load(json_file)
    return data