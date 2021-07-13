import json
import youtube_api as yt
from googleapiclient.discovery import build
from pandas import DataFrame
from pandas import concat
from random import sample
from functools import reduce
from os import listdir
from pprint import pprint

RUN_LOCALLY = 'yes'

def parse_response(json_response):

    # interesting data are stored in the items node
    items = json_response['items'][0]
    desired_nodes = ['id', 'contentDetails', 'snippet', 'statistics']

    # try also json_normalize
    video_data = dict()
    for nd in desired_nodes:
        if nd == 'id':
            video_data['video_id'] = items.get('id', 'NA')
        elif nd == 'contentDetails':
            video_data['definition'] =  items[nd].get('definition', 'NA')
            video_data['duration'] = items[nd].get('duration', 'NA')
        elif nd == 'snippet':
            video_data['cat_id'] = items[nd].get('categoryId', 'NA')
            video_data['ch_id'] = items[nd].get('channelId', 'NA')
            video_data['ch_title'] = items[nd].get('channelTitle', 'NA')
            video_data['audio_language'] = items[nd].get('defaultAudioLanguage', 'NA')
            video_data['description'] = items[nd].get('description', 'NA')
            video_data['live_content'] = items[nd].get('liveBroadcastContent', 'NA')
            video_data['publish_date'] = items[nd].get('publishedAt', 'NA')
            video_data['tags'] = items[nd].get('tags', '')
            video_data['title'] = items[nd].get('title', 'NA')
        else:
            video_data['comments'] = items[nd].get('commentCount', 'NA')
            video_data['dislikes'] = items[nd].get('dislikeCount', 'NA')
            video_data['likes'] = items[nd].get('likeCount', 'NA')
            video_data['views'] = items[nd].get('viewCount', 'NA')

    # otherwise pandas complains
    video_data['tags'] = ', '.join(video_data.get('tags'))

    return video_data

videos_data = list()

if RUN_LOCALLY == 'yes':

    responses = listdir('data/json-responses')

    for r in responses:
        json_file = open('data/json-responses/{}'.format(r), 'r')
        output = json.load(json_file)
        data = parse_response(output)
        videos_data.append(data)

else:
    # call the service
    yt_key = os.environ.get('YT_API_PSW')
    api_service_name = 'youtube'
    api_version = 'v3'

    youtube = build(serviceName = api_service_name, version = api_version, developerKey = yt_key)
    upload_id = yt.get_upload_id(youtube, channel_id = 'UCMOiTfbUXxUFqJJtCQGHrrA')
    video_id = yt.get_video_id(youtube, upload_id)

    for id in video_id:
        video_data = yt.get_video_data(service_obj, video_id = id)
        video_data = parse_response(video_data)
        videos_data.append(video_data)

cols = ['video_id', 'title', 'publish_date', 'description', 'ch_title', 'ch_id', 'cat_id',
        'live_content', 'duration', 'definition', 'views', 'likes',
        'dislikes', 'comments', 'language', 'tags']

def generate_df(videos_data, columns):
    video_df = DataFrame()
    for i, dict in enumerate(videos_data):
        video_data = DataFrame(dict, columns = cols, index = [i])
        video_df = concat([video_df, video_data])
    return video_df

video_df = generate_df(videos_data, columns = cols)
video_df.to_csv('data/boldrin-df.csv', index = False)
print(video_df)
