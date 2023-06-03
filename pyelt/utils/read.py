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
