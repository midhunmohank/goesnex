import requests

host_url = "http://127.0.0.1:8501"
host_url_api = "http://127.0.0.1:8000"

        
        
# Define a function to check if the user is authorized

url_token = f"{host_url_api}/token"
data = {'username': "johndoe", 'password': 'secret'}
response_token = requests.post(url_token, data=data)
print(response_token.json())