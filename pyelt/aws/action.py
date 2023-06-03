import os
import logging
import boto3
from botocore.exceptions import ClientError
from utils.read import load_json, read_config

def start_ec2(path='infra/ec2.json'):
    ec2_specs = load_json(path)
    id = ec2_specs['InstanceId']
    ec2 = boto3.client('ec2')
    
    # Do a dryrun first to verify permissions
    try:
        ec2.start_instances(InstanceIds=[id], DryRun=True)
    except ClientError as err:
        if 'DryRunOperation' not in str(err):
            raise

    # Dry run succeeded, run start_instances without dryrun
    try:
        response = ec2.start_instances(InstanceIds=[id], DryRun=False)
        print(response)
    except ClientError as err:
        print(err)

def stop_ec2(path='infra/ec2.json'):
    ec2_specs = load_json(path)
    id = ec2_specs['InstanceId']
    ec2 = boto3.client('ec2')
    
    # Do a dryrun first to verify permissions
    try:
        ec2.stop_instances(InstanceIds=[id], DryRun=True)
    except ClientError as err:
        if 'DryRunOperation' not in str(err):
            raise

    # Dry run succeeded, call stop_instances without dryrun
    try:
        response = ec2.stop_instances(InstanceIds=[id], DryRun=False)
        print(response)
    except ClientError as err:
        print(err)

def create_bucket(path_s3='infra/s3.json', path_creds='infra/pipeline.config'):
    """Create an S3 bucket

    :return: True if bucket created, else False
    """

    # Get S3 properties
    s3_specs = load_json(path_s3)
    region = s3_specs['region']
    bucket_name = s3_specs['bucketName']
    access_control = s3_specs['accessControl']
    account_full = s3_specs['grantFullControl']

    # Get AWS credentials
    creds = read_config(path_creds)
    access_key = creds['access_key']
    secret_access = creds['secret_key']

    # Create bucket
    try:
        s3_client = boto3.client(
            's3', 
            region_name=region, 
            aws_access_key_id = access_key, 
            aws_secret_access_key = secret_access
        )
        location = {'LocationConstraint': region}
        s3_client.create_bucket(
            ACL = access_control,
            Bucket=bucket_name, 
            CreateBucketConfiguration=location#,
            #GrantFullControl=account_full
        )
    except ClientError as err:
        logging.error(err)
        return False
    return True

def upload_file(file_name, path_s3='infra/s3.json', path_creds='infra/pipeline.config'):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :return: True if file was uploaded, else False
    """

    # Get S3 properties
    s3_specs = load_json(path_s3)
    region = s3_specs['region']
    bucket_name = s3_specs['bucketName']

    # Get AWS credentials
    creds = read_config(path_creds)
    access_key = creds['access_key']
    secret_access = creds['secret_key']

    # If S3 object_name was not specified, use file_name
    object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client(
        's3',
        region_name=region,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_access
    )
    try:
        s3_client.upload_file(
            file_name,
            bucket_name,
            object_name
        )
    except ClientError as err:
        logging.error(err)
        return False
    return True