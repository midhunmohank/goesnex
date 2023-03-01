import boto3
import json
import time
from datetime import datetime, timedelta
import time
import pandas as pd
import re

AWS_REGION = "us-east-1"
# client = boto3.client('logs', region_name=AWS_REGION)

client = boto3.client(
    'logs',
    aws_access_key_id="AKIAYHDNFRHDPCTAWVOG",
    aws_secret_access_key="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",
    region_name='us-west-1'
)


def add_user_logs(username, endpoint, payload, response_code):
    
    log_data = {
        "time" : time.time(), 
        "username" : username, 
        "endpoint" : endpoint,
        "payload" : payload, 
        "response_code" : response_code
    }
    
    
    response = client.put_log_events(
        logGroupName = 'goes-nex-logs',
        logStreamName = 'user-logs',
        logEvents=[
            {
                'timestamp': int(round(time.time() * 1000)),
                'message': str(log_data),
            }
        ]
    )
    
    print(response)
     
#add_user_logs("snehilaryan", "www.get.dummy", "no payload", 200)

query = f"""
    fields @timestamp, @message
    | filter @logStream = 'user-logs'
    | limit 100
"""


# response = client.start_query(
#     logGroupName="goes-nex-logs",
#     startTime=int((datetime.today() - timedelta(days=1)).timestamp()),
#     endTime=int(datetime.now().timestamp()),
#     queryString=query,
# )

# query_id = response['queryId']

# SLEEP_TIME = 3 # seconds

# results = client.get_query_results(queryId=query_id)

# time.sleep(SLEEP_TIME)

# while results['status'] == 'Running':
#     results = client.get_query_results(queryId=query_id)
#     time.sleep(SLEEP_TIME)

# # print(results['results'])

# lst = results['results']

# x = [lst[i][1]["value"] for i in range(0, len(lst))]
# print(x)
# def list2df(dct):
#     dct = []
#     for y in x:
#         y = y.replace("'", "\"")
#         y = y.replace('"{', "{")
#         y = y.replace('}"', "}")
#         y = json.loads(y)
#         y.pop('payload')
#         dct.append(y)
#     print(dct)
#     dct = pd.DataFrame(dct)
#     return dct
        
        
        
# df = list2df(x)

# df.to_csv("user_logs.csv")

df = pd.read_csv("user_logs.csv")
# print(df.head())


def get_api_count_lastday():
    return len(df)


def get_api_count_endpoint():
    x = df['endpoint'].value_counts()
    return x.to_json()

def get_api_count_response():
    x = df['response_code'].value_counts()
    return x.to_json()
    

    
print(get_api_count_endpoint())
# print(type(get_api_count_response()[455.0]))

    

# query = f"""
#     fields @timestamp, @message
#     | filter @logStream = 'user-logs'
#     | limit 10
# """

# response = client.start_query(
#     logGroupName="goes-nex-logs",
#     startTime=int((datetime.today() - timedelta(days=1)).timestamp()),
#     endTime=int(datetime.now().timestamp()),
#     queryString=query,
# )

# query_id = response['queryId']

# SLEEP_TIME = 3 # seconds

# results = client.get_query_results(queryId=query_id)

# time.sleep(SLEEP_TIME)

# while results['status'] == 'Running':
#     results = client.get_query_results(queryId=query_id)
#     time.sleep(SLEEP_TIME)

# # print(results['results'])

# lst = results['results']
# # lst = [[{'field': '@timestamp', 'value': '2023-03-01 00:37:53.004'}, {'field': '@message', 'value': '{\'time\': 1677631073.0038993, \'username\': \'snehilaryan\', \'endpoint\': \'/get_files_goes/\', \'payload\': "{\'year\': \'2022\', \'month\': \'09\', \'day\': \'13\', \'hour\': \'04\'}", \'response_code\': \'200\'}'}, {'field': '@ptr', 'value': 'ClkKHgoaNTY1MDE3MTUxOTQyOmdvZXMtbmV4LWxvZ3MQABI1GhgCBj2wamgAAAAAbtWM9gAGP+nl4AAAAIIgASjs1erU6TAw7NXq1OkwOAFA1wFI5AlQ5gQYABAAGAE='}], [{'field': '@timestamp', 'value': '2023-03-01 00:37:48.224'}, {'field': '@message', 'value': '{\'time\': 1677631068.2242174, \'username\': \'snehilaryan\', \'endpoint\': \'/get_hours_goes/\', \'payload\': "{\'year\': \'2022\', \'month\': \'09\', \'day\': \'13\'}", \'response_code\': \'200\'}'}, {'field': '@ptr', 'value': 'ClkKHgoaNTY1MDE3MTUxOTQyOmdvZXMtbmV4LWxvZ3MQARI1GhgCBj3hxwQAAAAAR7MBQQAGP+nf0AAAAkIgASjej+jU6TAwwLDq1OkwOAJAkgNItwpQuQUYABABGAE='}]]

# # for i in range(0, len(lst)):
    

# # print([lst[i][1]["value"] for i in range(0, len(lst))])

# x = [lst[i][1]["value"] for i in range(0, len(lst))]
# print(x)
# def list2df(dct):
#     dct = []
#     for y in x:
#         y = y.replace("'", "\"")
#         y = y.replace('"{', "{")
#         y = y.replace('}"', "}")
#         y = json.loads(y)
#         y.pop('payload')
#         dct.append(y)
#     print(dct)
#     dct = pd.DataFrame(dct)
#     return dct
        
        
        
# print(list2df(x))
# # print(type(x[0]))
# y = x[0]

# print(y)
# # data_dict = json.loads(y)
# y = y.replace("'", "\"")
# y = y.replace('"{', "{")
# y = y.replace('}"', "}")
# print(y)

# # # Convert the string to a dictionary
# data_dict = json.loads(y)

# def dict2df(dct):
#     dct.pop('payload')
#     dct = pd.DataFrame(dct, index = [1,2])
#     return dct

# x = dict2df(data_dict)
# print(x.head())


# data = [json.loads(s.replace('\'', '')) for s in x]
# print(data)

# Create a DataFrame from the list
# df = pd.DataFrame(x, columns=[''])

# print(df)
# # Print the data frame
# print(df)
# print(df.shape)




# def get_hour_metrics_goes():
#     response = client.get_log_events(
#         logGroupName="logs-goes-nexrad",
#         logStreamName="log_goes_search",
#         startFromHead=False
#     )

#     freq_hours = {i:0 for i in range(0, 24)}
#     for i in response["events"]:
#         y = i["message"]
#         y = y.replace("'", '"')
#         hour = int(json.loads(y)["options_selected"]["hour_selected"])
#         print(hour)
#         freq_hours[hour] = freq_hours[hour] + 1
    
#     return freq_hours


# def get_hour_metrics_nexrad():
#     response = client.get_log_events(
#         logGroupName="logs-goes-nexrad",
#         logStreamName="log_nexrad_search",
#         startFromHead=False
#     )

#     freq_hours = {i:0 for i in range(0, 24)}
#     for i in response["events"]:
#         y = i["message"]
#         y = y.replace("'", '"')
#         hour = int(json.loads(y)["options_selected"]["hour_selected"])
#         print(hour)
#         freq_hours[hour] = freq_hours[hour] + 1

#     print(freq_hours)
    


#get_hour_metrics_nexrad()