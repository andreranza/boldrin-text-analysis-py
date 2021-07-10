#!/usr/bin/env python3

import os
from googleapiclient.discovery import build

yt_key = os.environ.get('YT_API_PSW')

def try_execute(request_obj):
    """Execute the request and get a response."""
    try:
        ch_resp = request_obj.execute()
    except HttpError as e:
        print('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))
    return ch_resp


def obtain_response(n_output, dev_key, ch_username):
    """Returns a list containing the reponses resulting
    from consecutive calls made to playlistItems() resource of the YouTube API.
    """

    # create service object
    youtube = build(serviceName = 'youtube', version = 'v3', developerKey = yt_key)

    # call the resource 'channel' in order to get the id related to the upload playlist
    ch_req = youtube.channels().list(
        part = 'contentDetails',
        forUsername = ch_username
    )

    ch_resp = try_execute(ch_req)

    upload_id = ch_resp['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    # inizialize empty list to store API responses
    responses = list()

    # call the resource 'playlistItems' using the upload_id
    pl_req = youtube.playlistItems().list(
        part = 'contentDetails, snippet',
        maxResults = n_output,
        playlistId = upload_id
    )

    pl_resp = try_execute(pl_req)

    responses.append(pl_resp)

    # consecutive calls until None is returned
    while True:
        pl_req = youtube.playlistItems().list_next(pl_req, pl_resp)
        if pl_req != None:
            pl_resp = try_execute(pl_req)
            output.append(pl_resp)
        else:
            break

    youtube.close()

    return responses


if __name__ == '__main__':
    resp = obtain_response(n_output = 50, dev_key = yt_key, ch_username = 'MicheleBoldrin')
    print(resp)
    print(len(resp))
