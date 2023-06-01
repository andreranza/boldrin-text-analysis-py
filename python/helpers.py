from json import load

def load_json_file(path):
    with open(path, 'r') as json_file:
        data = load(json_file)
    return data