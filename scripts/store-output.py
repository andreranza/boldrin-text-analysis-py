import youtube_api as yt
import json

# open list with video id
with open('data/video-id.txt') as f:
    video_id = f.read()
    video_id = video_id.replace("'", "").split(", ")

# store json locally
for id in video_id:
    print(id)
    js_resp = yt.get_response(service_obj = youtube, video_id = id)
    resp = open('data/json-responses/{}.json'.format(id), 'w')
    resp = json.dump(js_resp, resp)
