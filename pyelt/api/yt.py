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
    except HttpError as err:
        print(
            "Error response status code: {0}, reason: {1}".format(
                err.status_code, err.error_details
            )
        )
    return ch_resp


def get_upload_id(service_obj, channel_id):
    """Get the upload id from the resource type 'channel'."""
    ch_req = service_obj.channels().list(part="contentDetails", id=channel_id)
    ch_resp = try_execute(ch_req)

    upload_id = ch_resp["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    return upload_id


def get_video_id(service_obj, upload_id):
    """Returns a collection of video IDs from the channel's list of uploaded videos"""
    video_id = list()
    pl_req = service_obj.playlistItems().list(
        part="snippet", maxResults=1, playlistId=upload_id
    )
    pl_resp = try_execute(pl_req)
    id = pl_resp["items"][0]["snippet"]["resourceId"]["videoId"]
    video_id.append(id)

    # list next returns None when there is not
    while True:
        pl_req = service_obj.playlistItems().list_next(pl_req, pl_resp)
        if pl_req != None:
            pl_resp = try_execute(pl_req)
            id = pl_resp["items"][0]["snippet"]["resourceId"]["videoId"]
            video_id.append(id)
        else:
            break
    return video_id


def get_response(service_obj, video_id):
    """Get JSON response from service"""
    vid_req = service_obj.videos().list(
        part="contentDetails, snippet, statistics, recordingDetails", id=video_id
    )
    vid_resp = try_execute(vid_req)
    return vid_resp


if __name__ == "__main__":
    import os
    from googleapiclient.discovery import build
    from pandas import DataFrame
    from random import sample
    from pprint import pprint

    # obtain dev key at: https://console.cloud.google.com/
    dev_key = os.environ.get("YT_API_PSW")
    api_service_name = "youtube"
    api_version = "v3"

    # create service object
    youtube = build(
        serviceName=api_service_name, version=api_version, developerKey=dev_key
    )

    upload_id = get_upload_id(youtube, "UCMOiTfbUXxUFqJJtCQGHrrA")
    print(upload_id)

    # list of id values
    video_id = get_video_id(youtube, upload_id)
    print(video_id)

    # sample a random id from video_id collection
    an_id = sample(video_id, 1)[0]
    print(an_id)

    video_json = get_response(youtube, video_id=an_id)
    pprint(video_json)

    youtube.close()
