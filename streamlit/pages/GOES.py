import sqlite3
import streamlit as st
import time as tm
from datetime import datetime, timedelta,time, date
# import helper_functions.goes_module
import requests
import helper

def format_hour_goes(hour):
    if len(hour) == 1:
        hour = "0" + hour
    return hour


def app():
    
    file_to_download = ''
    dest_url = ''
    api_host = "http://3.22.188.56:8000"
    access_token = st.session_state["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    selected_date = ''

    with st.form(key="my_form"):
        st.title("GOES-Dockerized")
        # Create a date input widget
        selected_date = st.date_input("Date:", min_value= datetime(2022, 5, 1) , max_value=date.today())
        # selected_time = st.time_input("Time:")
        if selected_date:
            submit_button = st.form_submit_button("Next")
            
        year = selected_date.strftime("%Y")
        month = selected_date.strftime("%m")
        day = selected_date.strftime("%d")
        
        hours = requests.get(f"{api_host}/get_hours_goes/{year}/{month}/{day}", headers = headers)
        hours = hours.json()["hours"]
        hours_stripped = sorted(hours)

        # Check if the selected date is in the database
        if not hours_stripped:
            st.warning("No data found for the selected date.")
        else:
            # Create a time input widget
            hours_stripped.insert(0,'Select')
            selected_time = 'Select'
            selected_time = st.selectbox("Hour", hours_stripped)

            search_fields = st.form_submit_button(label="Search")
            # Combine the selected date and time into a single datetime object
            if type(selected_time) == str:
                pass
            else:
                #selected_datetime = datetime.combine(selected_date, selected_time)
                year = selected_date.strftime("%Y")
                month = selected_date.strftime("%m")
                day = selected_date.strftime("%d")
                hour = str(selected_time)
                
                hour = format_hour_goes(hour)

                #APIed code 
                response_goes_files = requests.get(f"{api_host}/get_files_goes/{year}/{month}/{day}/{hour}", headers = headers)
                selected_files = dict(response_goes_files.json())["list_of_files"]
                st.write('Number of files found:',len(selected_files))
                file_to_download = st.selectbox("Please select file for download: ",selected_files)
                download = st.form_submit_button("Get URL")
                url = ("1", "1")
                if download:
                    payload = {"src_file_key":file_to_download, "src_bucket_name":"noaa-goes18", "dst_bucket_name":"goes-team6", "dataset":"GOES"}
                    print(payload)
                    response_s3 = requests.post(f"{api_host}/copy_to_s3/", params=payload, headers = headers)
                    response_s3 = response_s3.json()["url"]
                    st.write("Destination URL: " + response_s3[1])
                    st.write("Source URL: " + response_s3[0])

            

    with st.form("url_generator"):
        st.title("Search by Filename")
        filename = st.text_input("Please enter filename")
        url_button = st.form_submit_button("Generate URL")
        if url_button:
            try:
                split = filename.split('_')
                timeStamp = split[4][1:]
                year = timeStamp[:4]
                day = timeStamp[4:7] 
                hour = timeStamp[7:9]

                #APIed code
                x = "ABI-L1b-RadC" + "/" + timeStamp[:4] + "/" + timeStamp[4:7] + "/" +  timeStamp[7:9] + "/" + filename
                if (not helper.validate_filename_goes(filename)):
                    st.write("File Format Incorrect")
                elif (not helper.file_exists("noaa-goes18", x)):
                    st.write("File Does Not Exist")
    #                 cw_logs.add_logs_file("GOES", filename, "File Does Not Exist")
                else:
                    filename_url = requests.get(f"{api_host}/get_url_goes_original/{filename}", headers = headers)
                    url = dict(filename_url.json())["original url"]
                    st.write(url)
    #                 cw_logs.add_logs_file("GOES", filename, url)
            except:
                st.write("Invalid File Name")            


   
if "access_token" in st.session_state:        
    app()
else:
    st.write("Please Login")






# # http://34.138.242.155:8000/get_url_goes_original/OR_ABI-L1b-RadC-M6C01_G18_s20230100506171_e20230100508546_c20230100508584.nc

# #             x = "ABI-L1b-RadC" + "/" + timeStamp[:4] + "/" + timeStamp[4:7] + "/" +  timeStamp[7:9] + "/" + filename
# #             # Extracting the timestamp
# #             if (not helper.validate_filename_goes(filename)):
# #                 st.write("File Format Incorrect")
# #             elif (not helper.file_exists("noaa-goes18", x)):
# #                 st.write("File Does Not Exist")
# #                 cw_logs.add_logs_file("GOES", filename, "File Does Not Exist")
# #             else:
# #                 url = goes_module.get_url_goes_original(filename)
# #                 st.write(url)
# #                 cw_logs.add_logs_file("GOES", filename, url)
# #         except:
# #             st.write("Invalid File Name")


