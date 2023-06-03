import boto3
from botocore.exceptions import ClientError
from utils.read import load_json_file

def start_ec2(path='infra/ec2.json'):
    ec2_specs = load_json_file(path)
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
    ec2_specs = load_json_file(path)
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

