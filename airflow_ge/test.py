import boto3
from datetime import datetime



# Set the S3 bucket name and prefix
bucket_name = "noaa-goes18"
prefix = "ABI-L1b-RadC/"
# s3 = boto3.resource("s3",)
s3 = boto3.client("s3", aws_access_key_id ="AKIAZW4EPXNKYZJXKP7Q", aws_secret_access_key="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" )


def get_metadata_and_store(s3, bucket_name, prefix, last_updated):
    last_updated = datetime.strptime(last_updated, "%Y-%m-%d %H:%M:%S")
    names = []
    paginator = s3.get_paginator("list_objects_v2")
    page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

    # Loop through each page of objects
    for page in page_iterator:
        # Loop through each object in the page
        for obj in page.get("Contents", []):
            key = obj.get("Key")
            if key.endswith(".nc"):
                # Parse the file name to get the year and day of year
                parts = key.split("/")
                t = (int(parts[1]), int(parts[2]),int(parts[3]))
                file_date = datetime.strptime(f"{t[0]} {t[1]} {t[2]}", "%Y %j %H")
                # Check if the file is newer than the last updated date in Snowflake
                if file_date > last_updated:
                    names.append(key)
    return names

names = get_metadata_and_store(s3, bucket_name, prefix, "2023-03-02 00:00:00")
print(names)