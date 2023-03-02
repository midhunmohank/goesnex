import boto3

s3 = boto3.client(
    's3',
    aws_access_key_id="AKIAZW4EPXNKYZJXKP7Q",
    aws_secret_access_key="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",
)

def day_of_year(year, month, day):
    days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    if month == 2 and ((year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)):
        days_in_month[2] = 29
        
    day_of_year = sum(days_in_month[:month]) + day
    return str(day_of_year)

def get_files_goes(year, month, day, hour):
    day_year = day_of_year(int(year), int(month), int(day))
    
    if len(day_year) == 1:
        day_year = "0" + "0" + day_year
        
    elif len(day_year) == 2:
        day_year = "0" + day_year 
    
    product = "ABI-L1b-RadC"
    # s3 = boto3.client("s3")
    bucket_name = "noaa-goes18"
    if(year != "2022" and year != "2023"):
        print("Not a Valid Year")
    #    return "Not Valid Year"

    else:
        prefix =  product + "/" + str(year) + "/" + str(day_year) + "/" + str(hour) + "/"
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix = prefix)
        #print(response)
        objects = response.get("Contents", []) 
        x = [obj["Key"] for obj in objects]
        
        #print(x)

        # print(len(x))
        return x
    
def get_url_goes_original(filename):
    split = filename.split('_')
    # Extracting the timestamp
    timeStamp = split[4][1:]
    year = timeStamp[:4]
    day = timeStamp[4:7] 
    hour = timeStamp[7:9]

    #Extracting the Product Name
    productName = "ABI-L1b-RadC"
    #productName = productName.rsplit('-',1)[0][:-1]
    s3Bucket = split[2][1:3]
    link = f'https://noaa-goes{s3Bucket}.s3.amazonaws.com/{productName}/{year}/{day}/{hour}/{filename}'
    return link

#print(get_files_goes("2023", "01", "10", "05"))

#copy_to_s3('ABI-L1b-RadC/2022/342/00/OR_ABI-L1b-RadC-M6C16_G18_s20223420051170_e20223420053555_c20223420054003.nc', 'noaa-goes18', 'goes-team6')
# y = get_files_goes('2023', '01', '18', '19')
# print(y)
####################Debugging###########
# product = "ABI-L1b-RadC"
# year = '2023'
# month = '01'
# day = '18'
# hour = '19'
# s3 = boto3.client("s3")
# bucket_name = "noaa-goes18"

# day_year = day_of_year(int(year), int(month), int(day))

# if len(day_year) < 3:
#     day_year = "0" + day_year 
    
# prefix =  product + "/" + str(year) + "/" + str(day_year) + "/" + str(hour) + "/"
# response = s3.list_objects_v2(Bucket=bucket_name, Prefix = prefix)
# #print(response)
# objects = response.get("Contents", []) 
# x = [obj["Key"] for obj in objects]
# print(prefix)
# print(x)


#copy_to_s3('ABI-L1b-RadC/2023/018/19/OR_ABI-L1b-RadC-M6C16_G18_s20230181941184_e20230181943570_c20230181944055.nc', 'noaa-goes18', 'goes-team6')
#copy_to_s3(src_file_key, src_bucket_name, dst_bucket_name)
