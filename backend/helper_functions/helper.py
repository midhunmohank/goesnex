# import noes_module as nm
# import goes_module as gm
from helper_functions import goes_module as gm
from helper_functions import noes_module as nm
import boto3
import botocore
import re
import pandas as pd
df = pd.read_csv("Book.csv")
#Function to check if a file exists in the s3 bucket 
s3 = boto3.client(
    's3',
    aws_access_key_id="AKIAZW4EPXNKYZJXKP7Q",
    aws_secret_access_key="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",
)

def file_exists(bucket_name, object_key):
    
    #s3 = boto3.client("s3")
    try:
        s3.head_object(Bucket=bucket_name, Key=object_key)
    except botocore.exceptions.ClientError:
        return False
    return True


#Function to copy files to s3 bucket and get the url of source and destination 
def copy_to_s3(src_file_key, src_bucket_name, dst_bucket_name, dataset):
    #s3 = boto3.client("s3")
    s3.copy_object(Bucket=dst_bucket_name, CopySource={"Bucket": src_bucket_name, "Key": src_file_key}, Key=src_file_key.split("/")[-1])
    
    dest_url = "https://goes-team6.s3.amazonaws.com/" + src_file_key.split("/")[-1]
    
    if dataset == "NEXRAD":
        
        source_url = nm.get_url_nexrad_original(src_file_key.split("/")[-1])
        if not file_exists(dst_bucket_name, "NEXRAD/" + src_file_key.split("/")[-1]):
            s3.copy_object(Bucket=dst_bucket_name, CopySource={"Bucket": src_bucket_name, "Key": src_file_key}, Key="NEXRAD/" + src_file_key.split("/")[-1])
            
        else:
            print("File already exists")
        dest_url = "https://goes-team6.s3.amazonaws.com/NEXRAD/" + src_file_key.split("/")[-1]
            
    elif dataset == "GOES":
        
        source_url = gm.get_url_goes_original(src_file_key.split("/")[-1])
        if not file_exists(dst_bucket_name, "GOES/" + src_file_key.split("/")[-1]):
            s3.copy_object(Bucket=dst_bucket_name, CopySource={"Bucket": src_bucket_name, "Key": src_file_key}, Key="GOES/" + src_file_key.split("/")[-1])
            
        else:
            print("File already exists")
        dest_url = "https://goes-team6.s3.amazonaws.com/GOES/" + src_file_key.split("/")[-1]
        
    return [dest_url, source_url]


# def validate_filename_goes(filename):
#     pattern = re.compile(r"^OR_ABI-L1b-RadC-M6C\d{2}_G\d{2}_s\d{14}_e\d{14}_c\d{14}\.nc$")
#     return bool(pattern.match(filename))

# def validate_filename_nexrad(filename):
#     pattern = r"^[A-Z]{4}[0-9]{8}_[0-9]{6}_V[0-9]{2}$"
#     pattern2 = r"^[A-Z]{4}[0-9]{8}_[0-9]{6}_V[0-9]{2}_MDM$"
#     match1 = re.match(pattern, filename)
#     match2 = re.match(pattern2, filename)
#     return bool(match1) or bool(match2)

def map_viz(station):
    # df = pd.read_csv("Book.csv")
    for index, row in df.iterrows():
        if row['NAME'] == station:
            return row['NAME'], row['LAT'], row['LON']












# file_name = "XXUX20230110_042152_V06"
# x = file_name[4:8] + "/" + file_name[8:10] + "/" + file_name[10:12] + "/" + file_name[0:4] + "/" + file_name
# print(file_exists("noaa-nexrad-level2", x))

# filename = "KABX20230110_005604_V06"
# print(validate_filename_nexrad(filename))
# KDFX20221226_045314_V06
# KLRX20230117_063500_V06
# TTUL20220630_014416_V08
# TPHX20220419_083331_V08


###########################################################


# copy_to_s3("ABI-L1b-RadC/2022/213/19/OR_ABI-L1b-RadC-M6C01_G18_s20222131901172_e20222131903544_c20222131903577.nc", src_bucket_name, dst_bucket_name, dataset)






















