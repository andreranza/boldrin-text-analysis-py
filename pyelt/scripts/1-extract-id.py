from datetime import datetime
import logging
import boto3
from pyelt.utils.read import read_yt_key
from pyelt.api import yt

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

api_service_name = "youtube"
api_version = "v3"

# id pointing to the playlist of uploaded video
upload_id = yt.get_upload_id(service_obj=youtube, channel_id=CH_ID)
logging.info("Got the upload id")

# list of id, one for each uploaded video in a given channel
video_id = yt.get_video_id(service_obj=youtube, upload_id=upload_id)
logging.info("Retrieved list of videos id")

# iterate through the ids to get a json response
for id in enumerate(video_id):
    # get response in JSON format
    video_json = yt.get_response(service_obj=youtube, video_id=id)

s3 = boto3.client("s3", aws_access_key_id=access_key, aws_secret_access_key=secret_key)
logging.info("Connected to S3 bucket: {0}".format(bucket_name))

# upload file
s3.upload_file(export_file, bucket_name, export_file)
logging.info("Uploaded output to S3 bucket: {0}".format(bucket_name))

logging.info("Data extraction concluded")
