import requests
import streamlit as st
def add_to_logs_user(endpoint, payload, response_code, access_token):
    
    # if "access_token" in st.session_state:
        # access_token = st.session_state["access_token"]
    header = {"Authorization": f"Bearer {access_token}"}

    api_host = "http://3.17.64.250:8000"
    
    payload_log = {
       "endpoint" : endpoint, 
       "payload" : payload, 
       "response_code" : response_code 
    }
    response= requests.post(f"{api_host}/add_user_logs/", params=payload_log, headers = header)