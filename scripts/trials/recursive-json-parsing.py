import os
import json
from pprint import pprint
from random import sample
import pandas as pd
import csv
# list json saved locally
responses = os.listdir('data/json-responses')

items = list()
for r in responses:
    json_file = open('data/json-responses/{}'.format(r), 'r')
    output = json.load(json_file)
    items_node = output['items'][0]
    items.append(items_node)

def drill_json_down(json_file):
    for k, v in json_file.items():
        if not isinstance(v, dict):
            record = (k, v)
            yield record
        else:
            for d in drill_json_down(v):
                yield d

# create final df
dataframes = list()
for i, json in enumerate(items):
    video_data = list(drill_json_down(json))
    df = pd.DataFrame.from_dict(dict(video_data), orient = 'index')
    df = df.rename(columns = {0 : i})
    df = df.transpose()
    dataframes.append(df)

videos_df = pd.concat(dataframes)


exp_file = 'export_file.csv'

with open(exp_file, 'w') as fp:
    csvw = csv.writer(fp, delimiter = '|')
    csvw.writerows(videos_df)
fp.close()

videos_df.to_csv('data/recursive-df.csv', index = False)
print(videos_df)
