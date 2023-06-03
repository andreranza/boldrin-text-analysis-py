# retrieve data records from the 'items' node of json response recursively
def drill_json_down(json_file):
    for k, v in json_file.items():
        if not isinstance(v, dict):
            record = (k, v)
            yield record
        else:
            for d in drill_json_down(v):
                yield d
