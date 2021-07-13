import os
import json
from pprint import pprint
from random import sample

responses = os.listdir('data/json-responses')

items = list()
for r in responses:
    json_file = open('data/json-responses/{}'.format(r), 'r')
    output = json.load(json_file)
    items_node = output['items'][0]
    items.append(items_node)

sample_item = sample(items, 1)[0]
pprint(sample_item)

def drill_json_down(json_file):
    for k, v in json_file.items():
        if not isinstance(v, dict):
            record = {k: v}
            yield record
        else:
            for d in drill_json_down(v):
                yield d

video_data = list(drill_json_down(sample_item))
pprint(video_data)
