#!/usr/bin/python3

import typer   
import requests
import boto3
import configparser
import helper


host_url_api = "http://3.17.64.250:8000"

app = typer.Typer(name="mycli")
# api_host = "http://34.138.242.155:8000"
# for arg in sys.argv:
#     print(arg)

config = configparser.ConfigParser()
config.read("config.ini")
    
s3 = boto3.client(
    's3',
    aws_access_key_id="AKIAZW4EPXNKYZJXKP7Q",
    aws_secret_access_key="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",
)

# Test hello command 
@app.command()
def hello(name: str = typer.Argument("Anonymous"), lastname: str = typer.Option(..., prompt="Please enter your lastname", confirmation_prompt=True)):
    print(f"Hello {name} {lastname}")



# @app.command("user_login")
# def cli_user_login(username : str = typer.Option(..., prompt="Enter username"), password: str = typer.Option(..., prompt="Enter password", confirmation_prompt=True)):
#     payload = {"username":username, "password":password}
#     response = requests.post(f"{host_url_api}/token", params=payload)
#     print(response.json())

# access_token = ""

@app.command("user-login")
def cli_user_login(username: str = typer.Option(..., prompt="Enter username"), password: str = typer.Option(..., prompt="Enter passwrod" , confirmation_prompt=True)):
    url = f"{host_url_api}/token"
    data = {
        "username": username,
        "password": password
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        access_token = response.json()["access_token"]
        config["DEFAULT"]["access_token"] = access_token
        with open("config.ini", "w") as configfile:
            config.write(configfile)
        typer.echo(f"Logged in successfully.")
    else:
        typer.echo("Login failed. Please check your credentials.")

@app.command("user-signup")
def cli_user_signup(username: str = typer.Option(..., prompt="Enter username"), 
                    fullname: str = typer.Option(..., prompt="Enter full name"),
                    password: str = typer.Option(..., prompt="Enter password" , confirmation_prompt=True),
                    tier: str = typer.Option(..., prompt="Select tier: free, gold, platinum" )):
    url = f"{host_url_api}/create_user"
    data = {
        "USERNAME": username,
        "FULL_NAME": fullname,
        "TIER": tier,
        "HASHED_PASSWORD": password,
        "DISABLED": False
    }
    header = {
                        "Content-Type": "application/json",
                        "Accept": "application/json"
            }
    response = requests.post(url, json=data, headers=header)
    response = response.json()
    if response['status'] == True:
        typer.echo("User created successfully.")
    else:
        typer.echo("User creation failed. Please try again.")


@app.command("user-logout")
def logout():
    if "access_token" in config["DEFAULT"]:
        del config["DEFAULT"]["access_token"]
        with open("config.ini", "w") as configfile:
            config.write(configfile)
        typer.echo("Logout successful!")
    else:
        typer.echo("You are not currently logged in.")


def is_token_present():
    config = configparser.ConfigParser()
    config.read("config.ini")
    if "access_token" in config["DEFAULT"]:
        return True
    else:
        return False

@app.command('user-update-password')
def cli_user_update_password(
    old_password: str = typer.Option(..., prompt="Enter old password"),
    new_password: str = typer.Option(..., prompt="Enter new password", confirmation_prompt=True)):
    if is_token_present():
        access_token = config["DEFAULT"]["access_token"]
        header = {"Authorization": f"Bearer {access_token}"}
        response = requests.post(f"{host_url_api}/update_user/?old_password={old_password}&new_password={new_password}", headers=header)
        response = response.json()
        if response['status'] == True:
            typer.echo("Password updated successfully.")
    else:
        typer.echo("You are not currently logged in.")


# command to get the list of GOES file as per user input: year, month, day, hour
@app.command("get-files-goes")
def cli_get_files_goes(
    year: str = typer.Option(..., prompt="Enter year"),
    month: str = typer.Option(..., prompt="Enter month"),
    day: str = typer.Option(..., prompt="Enter day"),
    hour: str = typer.Option(..., prompt="Enter hour")):
    if is_token_present():
        access_token = config["DEFAULT"]["access_token"]
        header = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"{host_url_api}/get_files_goes/{year}/{month}/{day}/{hour}",headers=header)
        files = response.json()
        payload = str({"year":year, "month":month, "day":day, "hour":hour})
        helper.add_to_logs_user("/get_files_goes/", payload, response.status_code, access_token=access_token)
        print(files)
    else:
        typer.echo("You are not currently logged in.")


# response_nexrad_files = requests.get(f"{api_host}/get_files_noaa/{station}/{year}/{month}/{day}/{hour}", headers = headers)
# ayload_logs_3 = str({"year":year, "month":month, "day":day, "hour":hour, "station":station})
# helper.add_to_logs_user("/get_files_noaa/", payload_logs_3,  response_nexrad_files.status_code)
# command to get the public GOES file URL for a given filename
@app.command("get-public-url-goes")
def cli_get_url_goes_original(filename: str = typer.Option(..., prompt="Enter filename")):
    if is_token_present():
        access_token = config["DEFAULT"]["access_token"]
        header = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"{host_url_api}/get_url_goes_original/{filename}",headers=header)
        url = response.json()
        payload = str({"filename":filename})
        helper.add_to_logs_user("/get_url_goes_original/", payload, response.status_code, access_token=access_token)
        print(url)
    else:
        typer.echo("You are not currently logged in.")

# command to get the list of NEXRAD file as per user input: station, year, month, day, hour
@app.command("get-files-nexrad")
def cli_get_files_nexrad(
    station: str = typer.Option(..., prompt="Enter station code"), 
    year: str  = typer.Option(..., prompt="Enter year"), 
    month: str = typer.Option(..., prompt="Enter month"),
    day: str = typer.Option(..., prompt="Enter day"),
    hour: str = typer.Option(..., prompt="Enter hour")):
    access_token = config["DEFAULT"]["access_token"]
    header = {"Authorization": f"Bearer {access_token}"}
    if is_token_present():
        response = requests.get(f"{host_url_api}/get_files_noaa/{station}/{year}/{month}/{day}/{hour}",headers=header)
        files = response.json()
        payload = str({"station":station, "year":year, "month": month, "day":day, "hour":hour})
        helper.add_to_logs_user("/get_files_noaa/", payload, response.status_code, access_token=access_token)
        print(files)
    else:
        typer.echo("You are not currently logged in.")

# command to get the public GOES file URL for a given filename
@app.command("get-public-url-nexrad")
def cli_get_url_nexrad_original(filename: str = typer.Option(..., prompt="Enter filename")):
    if is_token_present():
        access_token = config["DEFAULT"]["access_token"]
        header = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"{host_url_api}/get_url_nexrad_original/{filename}",headers=header)
        url = response.json()
        payload = str({"filename":filename})
        helper.add_to_logs_user("/get_url_nexrad_original/", payload, response.status_code, access_token=access_token)
        print(url)
    else:
        typer.echo("You are not currently logged in.")


# command to copy file in our public S3 bucket and generate URL to it 
@app.command("get-mi6-url-goes")
def cli_copy_to_s3_goes(filepath: str = typer.Option(..., prompt="Enter filename")):
    if is_token_present():
        access_token = config["DEFAULT"]["access_token"]
        header = {"Authorization": f"Bearer {access_token}"}
        payload = {"src_file_key":filepath, "src_bucket_name":"noaa-goes18", "dst_bucket_name":"goes-team6", "dataset":"GOES"}
        response = requests.post(f"{host_url_api}/copy_to_s3/", params=payload,headers=header)
        urls = response.json()
        helper.add_to_logs_user("/copy_to_s3/", payload, response.status_code, access_token=access_token)
        print(urls)
    else:
        typer.echo("You are not currently logged in.")

# command to copy file in our public S3 bucket and generate URL to it 
@app.command("get-mi6-url-nexrad")
def cli_copy_to_s3_nexrad(filepath: str = typer.Option(..., prompt="Enter filename")):
    if is_token_present():
        access_token = config["DEFAULT"]["access_token"]
        header = {"Authorization": f"Bearer {access_token}"}
        payload = {"src_file_key":filepath, "src_bucket_name":"noaa-nexrad-level2", "dst_bucket_name":"goes-team6", "dataset":"NEXRAD"} 
        response = requests.post(f"{host_url_api}/copy_to_s3/", params=payload,headers=header)
        # response_s3 = requests.post(f"{api_host}/copy_to_s3/", params=payload)
        urls = response.json()
        # payload = str({"filepath":filepath})
        helper.add_to_logs_user("/copy_to_s3/", payload, response.status_code, access_token=access_token)
        print(urls)
    else:
        typer.echo("You are not currently logged in.")



if __name__ == "__main__":
    app()



# prog_name="mi6"