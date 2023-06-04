from datetime import datetime
import logging
from pyelt.utils.read import read_yt_key
from pyelt.api import yt
from pyelt.aws import actions

today = datetime.date(datetime.today())

# logging configurations
logging.basicConfig(
    filename="logs/elt-youtube-api-log_{0}.txt".format(str(today)),
    level=logging.DEBUG,
    format=" %(asctime)s - %(levelname) s - %(message)s",
)

# retrieve channel id
try:
    with open("channel_id.txt") as f:
        CH_ID = f.read().rstrip()
except FileNotFoundError:
    logging.warning("Not able to retrieve channel id")
    CH_ID = str(input("Please, provide the channel id: ")).rstrip()

yt_key = read_yt_key(path="infra/youtube_api_key.txt")
youtube_service = yt.call_api(yt_key, "youtube", "v3")

# id pointing to the playlist of uploaded video
upload_id = yt.get_upload_id(service_obj=youtube_service, channel_id=CH_ID)
logging.info("Got the upload id")

# list of id, one for each uploaded video in a given channel
video_id = yt.get_video_id(service_obj=youtube_service, upload_id=upload_id)
logging.info("Retrieved list of videos id")

# iterate through the ids to get a json response
for vid_id in video_id:
    # get response in JSON format
    video_json = yt.get_response(service_obj=youtube_service, video_id=vid_id)
    # upload file
    actions.upload_file(file_name=vid_id)
    logging.info("Upload Video Id to S3: {0}".format(vid_id))

logging.info("Data extraction concluded")
