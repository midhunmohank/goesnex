from fastapi.testclient import TestClient
from fastapi_test import app
import json
client  = TestClient(app)
import requests

#url_token = f"{host_url_api}/token"
data = {'username': "johndoe", 'password': "secret"}
response_token = client.post('/token/', data=data)
access_token = response_token.json()["access_token"]

headers = {"Authorization": f"Bearer {access_token}"}

def test_copy_to_s3_goes():
    response = client.post("/copy_to_s3/", headers = headers)
    file_to_download = "ABI-L1b-RadC/2022/252/09/OR_ABI-L1b-RadC-M6C03_G18_s20222520916158_e20222520918531_c20222520918572.nc"
    payload = {"src_file_key":file_to_download, "src_bucket_name":"noaa-goes18", "dst_bucket_name":"goes-team6", "dataset":"GOES"}
    exp_response = {'url': ['https://goes-team6.s3.amazonaws.com/GOES/OR_ABI-L1b-RadC-M6C03_G18_s20222520916158_e20222520918531_c20222520918572.nc', 'https://noaa-goes18.s3.amazonaws.com/ABI-L1b-RadC/2022/252/09/OR_ABI-L1b-RadC-M6C03_G18_s20222520916158_e20222520918531_c20222520918572.nc']}
    api_host = "http://127.0.0.1:8000"
    response_s3 = client.post("/copy_to_s3/", params=payload, headers = headers)
    assert response_s3.status_code == 200
    assert exp_response == response_s3.json()

# print(test_copy_to_s3_goes())

def test_get_files_goes_api():
    response = client.get("/get_files_goes/2022/09/09/09", headers = headers)
    assert response.status_code == 200
    f = open('backend/test_files_json/response_goes.json')
    expected_json = json.load(f)
    assert expected_json == response.json()

def test_get_url_goes_original():
    response = client.get("get_url_goes_original/OR_ABI-L1b-RadC-M6C01_G18_s20222961901174_e20222961903547_c20222961903582.nc", headers = headers)
    assert response.status_code == 200
    url = response.json()['original url']
    assert url == 'https://noaa-goes18.s3.amazonaws.com/ABI-L1b-RadC/2022/296/19/OR_ABI-L1b-RadC-M6C01_G18_s20222961901174_e20222961903547_c20222961903582.nc'


def test_get_files_noaa_api():
    response = client.get("get_files_noaa/KABR/2022/09/17/05", headers = headers)
    assert response.status_code == 200
    f = open('backend/test_files_json/response_nexrad.json')
    expected_json = json.load(f)
    assert expected_json == response.json()

def test_get_url_nexrad_original():
    response = client.get("get_url_nexrad_original/KABR20220917_050243_V06", headers = headers)
    assert response.status_code == 200
    url = response.json()['original url']
    assert url == 'https://noaa-nexrad-level2.s3.amazonaws.com/2022/09/17/KABR/KABR20220917_050243_V06'
    

def test_plot_map_viz():
    response = client.get("/map_visualization/KABR", headers = headers)
    assert response.status_code == 200
    exp_respose = {"name": "KABR", "lat": 45.455833, "lon": -98.413333}
    assert response.json() == exp_respose
    
    
    
    
