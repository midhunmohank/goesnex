import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from datetime import datetime, timedelta
import base64
import requests
import json
import helper

# Define the Streamlit app
def app():

    api_host = helper.get_api_host()
    access_token = st.session_state["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    activity_data = {
    "user1": {"2022-01-01": 10, "2022-01-02": 15, "2022-01-03": 12}
    }
    
    response_user = requests.get(f"{api_host}/users/me/", headers=headers)
    username = response_user.json()["USERNAME"]

    response_df = requests.get(f"{api_host}/api_user_df/{username}", headers=headers)
    json_str = response_df.json()

    data_dict = json.loads(json_str)
    # print(data_dict)

    logs_df = pd.DataFrame(data_dict)

    # Convert timestamp to date
    logs_df['date'] = pd.to_datetime(logs_df['time'], unit='s').dt.date

    # Group by date and count the number of entries in each group
    calls_per_day = logs_df.groupby('date').size().reset_index(name='count')


    #logs_df.drop('date',axis=1,inplace=True)
    logs_df['hour'] = pd.to_datetime(logs_df['time'],unit='s').dt.hour
    calls_per_hour = logs_df.groupby('hour').size().reset_index(name='count')


    logs_df.set_index('time', inplace=True)

    response = requests.get(f"{api_host}/api_count_endpoint/", headers=headers)

    json_str = response.json()

    data_dict = json.loads(json_str)



    endpoint_calls_data = pd.DataFrame({
        'endpoint': list(data_dict.keys()),
        'total_calls': list(data_dict.values())
    })





    # Add a title
    st.title("User Activity Dashboard")

    # Create a DataFrame from the activity data
    df = pd.DataFrame(activity_data)

    # Melt the DataFrame to convert it from wide to long format
    df = df.reset_index().melt(id_vars=["index"], var_name="user", value_name="activity")

    # Convert the date column to a datetime object
    df["index"] = pd.to_datetime(df["index"])

    # Add a line chart to visualize the user activity over time
    chart = alt.Chart(df).mark_line().encode(
        x="index:T",
        y="activity:Q",
        color="user:N"
    ).properties(
        width=600,
        height=300
    ).configure_axis(
        grid=False
    )

    st.altair_chart(chart)

    # Add a metric to show total API calls the previous day
    from datetime import datetime, timedelta

# Filter the DataFrame to only include calls from the last day
    # one_day_ago = datetime.now() - timedelta(days=1)
    # calls_per_day['date'] = pd.to_datetime(calls_per_day['date'])
    # mask = calls_per_day['date'] >= one_day_ago
    # df_filtered = calls_per_day[mask]

    # Group the filtered DataFrame by date and count the number of rows in each group
    # count_by_date = calls_per_day.groupby('date').count()
    # print(count_by_date)
    # count_yes = count_by_date["count"][count_by_date["date"] == one_day_ago]
    # print(count_by_date)
    # # Print the result
    print(calls_per_day)
    last_day_count = logs_df[logs_df['date'] >= pd.Timestamp.now().normalize() - pd.Timedelta(days=1)].shape[0]
    metric_col, metric_val, metric_vis = st.columns(3)
    with metric_col:
        st.subheader("Total API Calls Yesterday")
    with metric_val:
        st.metric(label="Total Calls Made Yesterday", value = last_day_count)
        st.metric(label="Total Calls Made in last 7 days", value = len(logs_df))
        st.metric(label = "Average Calls In the Last Week", value=calls_per_day["count"].mean())
        

    with metric_vis:
        st.subheader("Calls By The Hour")
        chart_data = calls_per_hour
        chart = alt.Chart(chart_data).mark_bar().encode(
            x='hour:T',
            y='count:Q'
        )
        st.altair_chart(chart)

    # Add a table to show the user activity data
    st.subheader("User Activity Data")
    st.dataframe(logs_df)


    # Add a bar chart to visualize the success and failed API calls over time
    
    calls_per_day_rate = logs_df.groupby(['date', 'response_code']).size().reset_index(name='count')
    
    df_new = (calls_per_day_rate.pivot(index='date', columns='response_code', values='count')
            .fillna(0)
            .rename(columns=lambda x: f"{x} cals")
            .reset_index())
    
    df_new.rename(columns={'200 cals': 'Success', '429': 'Failiure'}, inplace=True)
    
    st.dataframe(df_new)

    st.subheader("Comparison of Success")
    chart = alt.Chart(df_new).mark_bar().encode(
        x="date:T",
        y="Success:Q",
        color=alt.value("#2ecc71")
    ).properties(
        width=600,
        height=300
    )

    chart += alt.Chart(df_new).mark_bar().encode(
        x="date:T",
        y="Failiure:Q",
        color=alt.value("#e74c3c")
    ).properties(
        width=600,
        height=300
    )

    st.altair_chart(chart)

    # Add a bar chart to visualize the endpoint total number of calls
    st.subheader("Endpoint Total Number of Calls")
    chart = alt.Chart(endpoint_calls_data).mark_bar().encode(
        x=alt.X('endpoint:N', title='Endpoint'),
        y=alt.Y('total_calls:Q', title='Total Calls'),
        color=alt.Color('endpoint:N', scale=alt.Scale(scheme='set1'))
    ).properties(
        width=600,
        height=300
    ).configure_axis(
        grid=False
    )
    st.altair_chart(chart)

    # Add a download link for the user activity data
    csv = logs_df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="user_activity.csv">Download User Activity Data (CSV)</a>'
    st.markdown(href, unsafe_allow_html=True)

    # csv = total_api_calls_data.to_csv(index=False)
    # b64 = base64.b64encode(csv.encode()).decode()
    # href = f'<a href="data:file/csv;base64,{b64}" download="total_api_calls.csv">Download Total API Calls Data (CSV)</a>'
    # st.markdown(href, unsafe_allow_html=True)

    st.write("---")
    st.write(f"Dashboard last updated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")

if "access_token" in st.session_state:        
    app()
else:
    st.write("Please Login")
