import youtube_api as yt
import json
import configparser
import csv
import boto3
import os
import pandas as pd
from googleapiclient.discovery import build
from pprint import pprint

yt_key = os.environ.get('YT_API_PSW')
api_service_name = 'youtube'
api_version = 'v3'
CH_ID = 'UCMOiTfbUXxUFqJJtCQGHrrA'

# call the service
youtube = build(serviceName = api_service_name, version = api_version, developerKey = yt_key)

# id pointing to the playlist of uploaded video
upload_id = yt.get_upload_id(service_obj = youtube, channel_id = CH_ID)

# list of id, one for each uploaded video in a given channel
video_id = yt.get_video_id(service_obj = youtube, upload_id = upload_id)

# retrieve data records from the 'items' node of json response recursively
def drill_json_down(json_file):
    for k, v in json_file.items():
        if not isinstance(v, dict):
            record = (k, v)
            yield record
        else:
            for d in drill_json_down(v):
                yield d

# iterate through the ids to get a json response
dataframes = list()
for i, id in enumerate(video_id):
    # get response in JSON format
    video_json = yt.get_response(service_obj = youtube, video_id = id)

    # fetch 'items' node that contains relevant data
    items_node = video_json['items'][0]

    # parse response
    records = list(drill_json_down(items_node))

    # create dataframe from json
    df = pd.DataFrame.from_dict(dict(records), orient = 'index')
    df = df.rename(columns = {0 : i})
    df = df.transpose()
    dataframes.append(df)

# reduce list of dataframes into a single one
videos_df = pd.concat(dataframes)

export_file = 'data/recursive-df.csv'

# save file
videos_df.to_csv(export_file, index = False)

# load credentials
parser = configparser.ConfigParser()
parser.read('scripts/pipeline.config')
access_key = parser.get('aws_boto_credentials', 'access_key')
secret_key = parser.get('aws_boto_credentials', 'secret_key')
bucket_name = parser.get('aws_boto_credentials', 'bucket_name')

s3 = boto3.client(
    's3',
    aws_access_key_id = access_key,
    aws_secret_access_key = secret_key
    )

# upload file
s3.upload_file(export_file, bucket_name, export_file)
