import boto3
import snowflake.connector

s3 = boto3.client(
    's3',
    aws_access_key_id="AKIAZW4EPXNKYZJXKP7Q",
    aws_secret_access_key="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",
)

#Function to get files given the station, year, month day and hour
def get_files_noaa(station, year, month, day, hour):
    
    #s3 = boto3.client("s3")
    bucket_name = "noaa-nexrad-level2"
    if(year != "2022" and year != "2023"):
        print("Not a Valid Year")
        return "Not Valid Year"   
    else:
        prefix = year + "/" + month + "/" + day  + "/" + station
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix = prefix)
        objects = response.get("Contents", []) 
        files = [obj["Key"] for obj in objects]
        files_hour = []
        for i in files: 
            if(i.split("_")[1][:2] == hour):  
                files_hour.append(i) 
        return files_hour
  
#Get the url from noaa website   
def get_url_nexrad_original(file_name):
    return "https://noaa-nexrad-level2.s3.amazonaws.com/" + file_name[4:8] + "/" + file_name[8:10] + "/" + file_name[10:12] + "/" + file_name[0:4] + "/" + file_name

conn = snowflake.connector.connect(
    user='SANJAYKASHYAP',
    password='Bigdata@23',
    account='iogoldm-vcb38713',
    warehouse='COMPUTE_WH',
    database='SEVIR_META',
    schema='PUBLIC'
)


def get_stations(year, month, day):
    cursor = conn.cursor()
    cursor.execute(f'select "station_name" from noes where "year" = {year} and "month" = {month} and "day" = {day}')
    return [i[0] for i in cursor.fetchall()]

# def states_from_stations(stations):
    
# state_codes = pd.read_excel("streamlit/pages/nexrad.xlsx").dropna()
# state_codes = state_codes[["NAME", "ST"]]


#print(get_stations("2022", "11", "01")) 
    
   
   
   
   
   
   
   
   
   
   
   
   
  #Debugging Code   
# https://noaa-nexrad-level2.s3.amazonaws.com//KEY/X2/02/KEYX/KEYX/KEYX20230105_000719_V06
# https://noaa-nexrad-level2.s3.amazonaws.com/2023/01/05/KEYX/KEYX20230105_000719_V06

# file_name = KEYX20230105_000719_V06
# print("year-" + file_name[4:8])
# print("month-" + file_name[8:10])
# print("day-" + file_name[10:12])
# print("station-" + file_name[0:4])



# print(get_url_noaa_original('KBIS20001222_090728.gz'))


#print(get_files_noaa("KBHX", "2022", "11", "01", "05"))






    
    
    

