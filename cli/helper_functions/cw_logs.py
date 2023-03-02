import boto3
import json
import time
import json
AWS_REGION = "us-east-1"
client = boto3.client('logs', region_name=AWS_REGION)


def add_logs_goes_search(date_selected, hour_selected, file_selected, source_output, destination_output):
    
    log_data = {
        "Time" : time.time(), 
        "Dataset" : "GEOS", 
        "options_selected" : {
            "date_selected" : date_selected, 
            "hour_selected" : hour_selected, 
            "file_selected" : file_selected
        }, 
        "output" : {
            "source_output" : source_output, 
            "destination" : destination_output
        }    
    }
    
    response = client.put_log_events(
        logGroupName = 'logs-goes-nexrad',
        logStreamName = 'log_goes_search',
        logEvents=[
            {
                'timestamp': int(round(time.time() * 1000)),
                'message': str(log_data)
            }
        ]
    )
    
def add_logs_nexrad_search(date_selected, hour_selected, state_selected, station_selected, file_selected, source_output, destination_output):
    
    log_data = {
        "Time" : time.time(), 
        "Dataset" : "NEXRAD", 
        "options_selected" : {
            "date_selected" : date_selected, 
            "hour_selected" : hour_selected,
            "state_selected" : state_selected, 
            "station_selected" : station_selected, 
            "file_selected" : file_selected
        }, 
        "output" : {
            "source_output" : source_output, 
            "destination" : destination_output
        }    
    }
    
    response = client.put_log_events(
        logGroupName = 'logs-goes-nexrad',
        logStreamName = 'log_nexrad_search',
        logEvents=[
            {
                'timestamp': int(round(time.time() * 1000)),
                'message': str(log_data)
            }
        ]
    )
    
def add_logs_file(dataset, file_name, output_url):
    
    log_data = {
        "time" : time.time(), 
        "dataset" : dataset, 
        "file_name" : file_name,
        "output_url" : output_url
    }
    
    response = client.put_log_events(
        logGroupName = 'logs-goes-nexrad',
        logStreamName = 'log_url_from_file',
        logEvents=[
            {
                'timestamp': int(round(time.time() * 1000)),
                'message': str(log_data)
            }
        ]
    )
    
def get_hour_metrics_goes():
    response = client.get_log_events(
        logGroupName="logs-goes-nexrad",
        logStreamName="log_goes_search",
        startFromHead=False
    )

    freq_hours = {i:0 for i in range(0, 24)}
    for i in response["events"]:
        y = i["message"]
        y = y.replace("'", '"')
        hour = int(json.loads(y)["options_selected"]["hour_selected"])
        print(hour)
        freq_hours[hour] = freq_hours[hour] + 1
    
    return freq_hours


def get_hour_metrics_nexrad():
    response = client.get_log_events(
        logGroupName="logs-goes-nexrad",
        logStreamName="log_nexrad_search",
        startFromHead=False
    )

    freq_hours = {i:0 for i in range(0, 24)}
    for i in response["events"]:
        y = i["message"]
        y = y.replace("'", '"')
        hour = int(json.loads(y)["options_selected"]["hour_selected"])
        print(hour)
        freq_hours[hour] = freq_hours[hour] + 1

    print(freq_hours)

#get_hour_metrics_nexrad()