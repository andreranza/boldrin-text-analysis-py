"""
The module provides functions to retrieve data from a YouTube channel's list of
uploaded videos given a service object.

To create a service object for a Google service see:
https://github.com/googleapis/google-api-python-client/blob/master/docs/start.md

Find specific methods to handle YouTube service objects at:
https://googleapis.github.io/google-api-python-client/docs/dyn/youtube_v3.html
"""

def try_execute(request_obj):
    """Execute the request and get a response."""
    try:
        ch_resp = request_obj.execute()
    except HttpError as e:
        print('Error response status code: {0}, reason: {1}'.format(e.status_code, e.error_details))
    return ch_resp


def get_upload_id(service_obj, channel_id):
    """Get the upload id from the resource type 'channel'."""
    ch_req = service_obj.channels().list(part = 'contentDetails', id = channel_id)
    ch_resp = try_execute(ch_req)

    upload_id = ch_resp['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    return upload_id


def get_video_id(service_obj, upload_id):
    """Returns a collection of video IDs from the channel's list of uploaded videos"""
    video_id = list()
    pl_req = service_obj.playlistItems().list(
        part = 'snippet',
        maxResults = 1,
        playlistId = upload_id
    )
    pl_resp = try_execute(pl_req)
    id = pl_resp['items'][0]['snippet']['resourceId']['videoId']
    video_id.append(id)

    # list next returns None when there is not
    while True:
        pl_req = youtube.playlistItems().list_next(pl_req, pl_resp)
        if pl_req != None:
            pl_resp = try_execute(pl_req)
            id = pl_resp['items'][0]['snippet']['resourceId']['videoId']
            video_id.append(id)
        else:
            break
    return video_id


def get_video_data(service_obj, video_id):

    vid_req = service_obj.videos().list(
        part = 'contentDetails, snippet, statistics, recordingDetails',
        id = video_id
    )

    vid_resp = try_execute(vid_req)

    items = vid_resp['items'][0]
    snippet = items['snippet']
    content_details = items['contentDetails']
    stats = items['statistics']
    rec_details = items['recordingDetails']

    video_data = dict()

    video_data['title'] = snippet['title']
    video_data['publish_date'] = snippet['publishedAt']
    video_data['description'] = snippet['description']
    video_data['ch_title'] = snippet['channelTitle']
    video_data['cat_id'] = snippet['categoryId']
    video_data['is_live'] = snippet['liveBroadcastContent']
    video_data['language'] = snippet['defaultAudioLanguage']
    video_data['duration'] = content_details['duration']
    video_data['definition'] = content_details['definition']
    video_data['views'] = stats['viewCount']
    video_data['likes'] = stats['likeCount']
    video_data['dislikes'] = stats['dislikeCount']
    video_data['comments'] = stats['commentCount']
    video_data['rec_date'] = rec_details['recordingDate']

    return video_data

if __name__ == '__main__':

    import os
    from googleapiclient.discovery import build
    from pandas import DataFrame

    # obtain dev key at: https://console.cloud.google.com/
    dev_key = os.environ.get('YT_API_PSW')
    api_service_name = 'youtube'
    api_version = 'v3'

    # create service object
    youtube = build(serviceName = api_service_name, version = api_version, developerKey = dev_key)

    upload_id = get_upload_id(youtube, 'UCMOiTfbUXxUFqJJtCQGHrrA')
    print(upload_id)

    video_id = get_video_id(youtube, upload_id)
    print(video_id)

    video_data = get_video_data(youtube, video_id[0])
    print(video_data)

    video_data = DataFrame(
        video_data,
        columns = ['title', 'publish_date', 'description', 'ch_title', 'cat_id',
                    'is_live', 'language', 'duration', 'definition', 'views', 'likes',
                    'dislikes', 'comments', 'rec_date'],
        index = [0]
    )
    print(video_data)

    video_data.to_csv('data/trial-video.csv', sep = ';', index = False)

    youtube.close()
