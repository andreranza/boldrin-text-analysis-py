import youtube_api as yt
import json
import configparser
import boto3
import os
import logging
import pandas as pd
from datetime import datetime
from googleapiclient.discovery import build

today = datetime.date(datetime.today())

# logging configurations
logging.basicConfig(
    filename='logs/elt-youtube-api-log_{0}.txt'.format(str(today)),
    level=logging.DEBUG, format=' %(asctime)s - %(levelname) s - %(message)s'
)

# retrieve API credentials
try:
    #yt_key = os.environ.get('YT_API_PSW')
    with open('yt-api-psw.txt') as f:
        yt_key = f.read().rstrip()
except FileNotFoundError:
    logging.warning('Not able to API credentials id locally')
    yt_key = str(input('Please, provide the API service key: ')).rstrip()


# retrieve channel id
try:
    with open('channel_id.txt') as f:
        CH_ID = f.read().rstrip()
except FileNotFoundError:
    logging.warning('Not able to retrieve channel id')
    CH_ID = str(input('Please, provide the channel id: ')).rstrip()

api_service_name = 'youtube'
api_version = 'v3'

# call the service
youtube = build(serviceName=api_service_name, version=api_version, developerKey=yt_key)
logging.info('Called the YouTube API Service')

# id pointing to the playlist of uploaded video
upload_id = yt.get_upload_id(service_obj=youtube, channel_id=CH_ID)
logging.info('Got the upload id')

# list of id, one for each uploaded video in a given channel
video_id = yt.get_video_id(service_obj=youtube, upload_id=upload_id)
logging.info('Retrieved list of videos id')

# iterate through the ids to get a json response
dataframes = list()
for i, id in enumerate(video_id):
    # get response in JSON format
    video_json = yt.get_response(service_obj=youtube, video_id=id)

    # fetch 'items' node that contains relevant data
    items_node = video_json['items'][0]

    # parse response
    records = list(drill_json_down(items_node))

    # create dataframe from json
    df = pd.DataFrame.from_dict(dict(records), orient='index')
    df = df.rename(columns={0: i})
    df = df.transpose()
    dataframes.append(df)

# reduce list of dataframes into a single one
videos_df = pd.concat(dataframes)

# add timestams
videos_df = videos_df.assign(timestamp=datetime.now())

# extract channel name
ch_name = videos_df.loc[1, 'channelTitle']
export_file = 'data/{0}_{1}.csv'.format(str(today), ch_name).replace(' ', '')

# save file
videos_df.to_csv(export_file, index=False)
logging.info('Saved output locally in {0}'.format(export_file))

# load credentials
parser = configparser.ConfigParser()
parser.read('scripts/pipeline.config')
access_key = parser.get('aws_boto_credentials', 'access_key')
secret_key = parser.get('aws_boto_credentials', 'secret_key')
bucket_name = parser.get('aws_boto_credentials', 'bucket_name')

s3 = boto3.client(
    's3',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key
)
logging.info('Connected to S3 bucket: {0}'.format(bucket_name))

# upload file
s3.upload_file(export_file, bucket_name, export_file)
logging.info('Uploaded output to S3 bucket: {0}'.format(bucket_name))

logging.info('Data extraction concluded')
