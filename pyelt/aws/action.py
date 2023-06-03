import boto3
import logging
from botocore.exceptions import ClientError
from utils.read import load_json, read_config

def start_ec2(path='infra/ec2.json'):
    ec2_specs = load_json(path)
    id = ec2_specs['InstanceId']
    ec2 = boto3.client('ec2')
    
    # Do a dryrun first to verify permissions
    try:
        ec2.start_instances(InstanceIds=[id], DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    # Dry run succeeded, run start_instances without dryrun
    try:
        response = ec2.start_instances(InstanceIds=[id], DryRun=False)
        print(response)
    except ClientError as e:
        print(e)

def stop_ec2(path='infra/ec2.json'):
    ec2_specs = load_json(path)
    id = ec2_specs['InstanceId']
    ec2 = boto3.client('ec2')
    
    # Do a dryrun first to verify permissions
    try:
        ec2.stop_instances(InstanceIds=[id], DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    # Dry run succeeded, call stop_instances without dryrun
    try:
        response = ec2.stop_instances(InstanceIds=[id], DryRun=False)
        print(response)
    except ClientError as e:
        print(e)

def create_bucket(paths={'s3': 'infra/s3.json', 'creds': 'infra/pipeline.config'}):
    """Create an S3 bucket

    :return: True if bucket created, else False
    """

    # Get S3 properties
    path_s3 = paths['s3']
    s3_specs = load_json(path_s3)
    region = s3_specs['region']
    bucket_name = s3_specs['bucketName']
    access_control = s3_specs['accessControl']
    account_full = s3_specs['grantFullControl']

    # Get AWS credentials
    path_creds = paths['creds']
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
    except ClientError as e:
        logging.error(e)
        return False
    return True
