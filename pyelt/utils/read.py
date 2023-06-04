import logging
from json import load
from configparser import ConfigParser


def load_json(path):
    with open(path, "r") as json_file:
        data = load(json_file)
    return data


def read_config(path="infra/pipeline.config"):
    # load credentials
    parser = ConfigParser()
    parser.read(path)
    access_key = parser.get("aws_boto_credentials", "access_key")
    secret_key = parser.get("aws_boto_credentials", "secret_key")
    return {"access_key": access_key, "secret_key": secret_key}

def read_yt_key(path="infra/youtube_api_key.txt"):
    """Read YouTube v3 Key

    :param path: Path to API key
    :return: API Key as a str
    """
    try:
        # yt_key = os.environ.get('YT_API_PSW')
        with open(path, "r", encoding="UTF-8") as file:
            yt_key = file.read().rstrip()
            return yt_key
    except FileNotFoundError:
        logging.warning("Not able to API credentials id locally")
        yt_key = str(input("Please, provide the API service key: ")).rstrip()

def read_channel_id(path="infra/channel-id.txt"):
    """Read Channel ID to choose on which channel to run the pipeline

    :param path: Path to channel id
    :return: str
    """
    try:
        with open(path, encoding="UTF-8") as file:
            channel_id = file.read().rstrip()
            return channel_id
    except FileNotFoundError:
        logging.warning("Not able to retrieve channel id")
        channel_id = str(input("Please, provide the channel id: ")).rstrip()
