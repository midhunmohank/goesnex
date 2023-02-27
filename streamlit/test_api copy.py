import requests 

host = "http://localhost:8000"
url_token = f"{host}/token"
data = {'username': 'johndoe', 'password': 'secret'}
response_token = requests.post(url_token, data=data)

print(response_token.json())
access_token = response_token.json()["access_token"]
headers = {"Authorization": f"Bearer {access_token}"}
# res = requests.get(f"http://127.0.0.1:8000/get_hours_goes/2022/11/09", headers = headers)
# print(res.json['hours'])
# print(res.json()["hours"])
# res = requests.get(f"http://127.0.0.1:8000/get_stations/2022/11/09", headers = headers)
# # print(res.json['hours'])
# print(res.json())
