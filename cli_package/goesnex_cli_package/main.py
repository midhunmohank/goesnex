#!/usr/bin/python3

import typer
import requests
import boto3
from helper_functions import helper
from helper_functions import noes_module as nm
from helper_functions import goes_module as gm

app = typer.Typer(name="mycli")
# api_host = "http://34.138.242.155:8000"
# for arg in sys.argv:
#     print(arg)

    
s3 = boto3.client(
    's3',
    aws_access_key_id="AKIAZW4EPXNKYZJXKP7Q",
    aws_secret_access_key="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",
)

# Test hello command 
@app.command()
def hello(name: str = typer.Argument("Anonymous"), lastname: str = typer.Option(..., prompt="Please enter your lastname", confirmation_prompt=True)):
    print(f"Hello {name} {lastname}")

# command to get the list of GOES file as per user input: year, month, day, hour
@app.command("get-files-goes")
def cli_get_files_goes(
    year: str = typer.Option(..., prompt="Enter year"),
    month: str = typer.Option(..., prompt="Enter month"),
    day: str = typer.Option(..., prompt="Enter day"),
    hour: str = typer.Option(..., prompt="Enter hour")):
    response = requests.get(f"http://127.0.0.1:8000/get_files_goes/{year}/{month}/{day}/{hour}")
    files = response.json()
    print(files)
    
# command to get the public GOES file URL for a given filename
@app.command("get-public-url-goes")
def cli_get_url_goes_original(filename: str = typer.Option(..., prompt="Enter filename")):
    response = requests.get(f"http://127.0.0.1:8000/get_url_goes_original/{filename}")
    url = response.json()
    print(url)

# command to get the list of NEXRAD file as per user input: station, year, month, day, hour
@app.command("get-files-nexrad")
def cli_get_files_nexrad(
    station: str = typer.Option(..., prompt="Enter station code"), 
    year: str  = typer.Option(..., prompt="Enter year"), 
    month: str = typer.Option(..., prompt="Enter month"),
    day: str = typer.Option(..., prompt="Enter day"),
    hour: str = typer.Option(..., prompt="Enter hour")):
    response = requests.get(f"http://127.0.0.1:8000/get_files_noaa/{station}/{year}/{month}/{day}/{hour}")
    files = response.json()
    print(files)

# command to get the public GOES file URL for a given filename
@app.command("get-public-url-nexrad")
def cli_get_url_nexrad_original(filename: str = typer.Option(..., prompt="Enter filename")):
    response = requests.get(f"http://127.0.0.1:8000/get_url_nexrad_original/{filename}")
    url = response.json()
    print(url)


# command to copy file in our public S3 bucket and generate URL to it 
@app.command("get-mi6-url-goes")
def cli_copy_to_s3_goes(filepath: str = typer.Option(..., prompt="Enter filename")):
    payload = {"src_file_key":filepath, "src_bucket_name":"noaa-goes18", "dst_bucket_name":"goes-team6", "dataset":"GOES"}
    response = requests.post(f"http://127.0.0.1:8000/copy_to_s3/", params=payload)
    urls = response.json()
    print(urls)

# command to copy file in our public S3 bucket and generate URL to it 
@app.command("get-mi6-url-nexrad")
def cli_copy_to_s3_nexrad(filepath: str = typer.Option(..., prompt="Enter filename")):
    payload = {"src_file_key":filepath, "src_bucket_name":"noaa-nexrad-level2", "dst_bucket_name":"goes-team6", "dataset":"NEXRAD"} 
    response = requests.post(f"http://127.0.0.1:8000/copy_to_s3/", params=payload)
    # response_s3 = requests.post(f"{api_host}/copy_to_s3/", params=payload)
    urls = response.json()
    print(urls)



if __name__ == "__main__":
    app()



# prog_name="mi6"