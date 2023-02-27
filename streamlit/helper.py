import boto3
import botocore
import re
 
 
s3 = boto3.client(
    's3',
    aws_access_key_id="AKIAZW4EPXNKYZJXKP7Q",
    aws_secret_access_key="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"
)

def file_exists(bucket_name, object_key):
    
    #s3 = boto3.client("s3")
    try:
        s3.head_object(Bucket=bucket_name, Key=object_key)
    except botocore.exceptions.ClientError:
        return False
    return True


def validate_filename_goes(filename):
    pattern = re.compile(r"^OR_ABI-L1b-RadC-M6C\d{2}_G\d{2}_s\d{14}_e\d{14}_c\d{14}\.nc$")
    return bool(pattern.match(filename))

def validate_filename_nexrad(filename):
    pattern = r"^[A-Z]{4}[0-9]{8}_[0-9]{6}_V[0-9]{2}$"
    pattern2 = r"^[A-Z]{4}[0-9]{8}_[0-9]{6}_V[0-9]{2}_MDM$"
    match1 = re.match(pattern, filename)
    match2 = re.match(pattern2, filename)
    return bool(match1) or bool(match2)