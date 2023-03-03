import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from datetime import datetime, timedelta
import base64
import requests
import json

# Define the Streamlit app
def app():

    api_host = "http://backapifast:8000"
    access_token = st.session_state["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    # Get today's date
    today = datetime.today()

    # Calculate yesterday's date
    yesterday = today - timedelta(days=1)

    # Dummy data for user countAPI 
    activity_data = {
    "user1": {"2022-01-01": 10, "2022-01-02": 15, "2022-01-03": 12}
    }

    # Create a dummy data for total API calls
    # total_api_calls_data = pd.DataFrame({
    #     'date': pd.date_range(datetime.today() - timedelta(days=8), periods=8),
    #     'total_api_calls': np.random.randint(low=100, high=200, size=(8,))
    # })

    # # Dummy data for SUCCESS/FAILURE API request calls
    # api_calls_data = pd.DataFrame({
    #     'date': pd.date_range(datetime.today() - timedelta(days=8), periods=8),
    #     'success_calls': np.random.randint(low=50, high=150, size=(8,)),
    #     'failed_calls': np.random.randint(low=0, high=50, size=(8,))
    # })


    response_user = requests.get(f"{api_host}/users/me/", headers=headers)
    print(response_user.json())
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

    print(calls_per_day)
    #logs_df.drop('date',axis=1,inplace=True)
    logs_df['hour'] = pd.to_datetime(logs_df['time'],unit='s').dt.hour
    calls_per_hour = logs_df.groupby('hour').size().reset_index(name='count')
    print(calls_per_hour)

    #FOR SUCCESS 200 
    calls_per_day_rate = logs_df.groupby(['date', 'response_code']).size().reset_index(name='count')
    print(calls_per_day_rate)
    calls_per_day_rate['success_calls_count'] = calls_per_day_rate[calls_per_day_rate['response_code'] == 200.0]['count'].sum()
    calls_per_day_rate['failed_calls_count'] = calls_per_day_rate[calls_per_day_rate['response_code'] != 200.0]['count'].sum()

    # Set date column as index
    logs_df.set_index('time', inplace=True)



    response = requests.get(f"{api_host}/api_count_endpoint/", headers=headers)

    json_str = response.json()

    data_dict = json.loads(json_str)
    print(data_dict)
    # Create a dataframe from the dictionary
    # endpoint_calls_data = pd.DataFrame(data_dict, index = [0]).T
    # print(endpoint_calls_data.head())



    # Dummy data for endpoint total number of calls
    endpoint_calls_data = pd.DataFrame({
        'endpoint': list(data_dict.keys()),
        'total_calls': list(data_dict.values())
    })

    print(endpoint_calls_data.head())

    # Generate dummy data for total API calls
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    total_api_calls = np.random.randint(low=100, high=1000, size=30)
    total_api_calls_data = pd.DataFrame({'date': dates, 'total_api_calls': total_api_calls})
    # total_api_calls_per_hr = 
    print(logs_df.head())
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
    yesterday = datetime.now() - timedelta(days=1)
    prev_day_calls_data = total_api_calls_data[(total_api_calls_data['date'] >= yesterday) & (total_api_calls_data['date'] < datetime.now())]
    prev_day_calls =  requests.get(f"{api_host}/api_count_lastday/", headers=headers).json()

    week_ago = datetime.now() - timedelta(days=7)
    prev_day_calls_week_ago_data = total_api_calls_data[(total_api_calls_data['date'] >= week_ago) & (total_api_calls_data['date'] < datetime.now() - timedelta(days=1))]
    prev_day_calls_week_ago = prev_day_calls_week_ago_data['total_api_calls'].sum() if len(prev_day_calls_week_ago_data) > 0 else 0

    metric_col, metric_val, metric_vis = st.columns(3)
    with metric_col:
        st.subheader("Total API Calls Yesterday")
    with metric_val:
        st.metric(label="", value=prev_day_calls, delta="+" + str(prev_day_calls - prev_day_calls_week_ago))
        if prev_day_calls > prev_day_calls_week_ago:
            st.write("🚀 Increased from last week")
        elif prev_day_calls < prev_day_calls_week_ago:
            st.write("🔻 Decreased from last week")
        else:
            st.write("🤝 Same as last week")
    with metric_vis:
        st.subheader("Total Average Calls Last Week")
        chart_data = calls_per_day
        chart = alt.Chart(chart_data).mark_line().encode(
            x='date:T',
            y='count:Q'
        )
        st.altair_chart(chart)

    with metric_vis:
        st.subheader("Total Average Calls PER HOUR")
        chart_data = calls_per_hour
        chart = alt.Chart(chart_data).mark_bar().encode(
            x='hour:T',
            y='count:Q'
        )
        st.altair_chart(chart)

    # Add a table to show the user activity data
    st.subheader("User Activity Data")
    st.dataframe(logs_df)
    # Add a stacked bar chart to visualize successful and failed API request calls
    # chart_data = api_calls_data.set_index('date').stack().reset_index().rename(columns={'level_1': 'status', 0: 'count'})
    # chart_data['status'] = chart_data['status'].str.replace('_calls', '').str.title()

    # chart = alt.Chart(chart_data).mark_bar().encode(
    #     x=alt.X('date:T', title='Date'),
    #     y=alt.Y('sum(count):Q', title='Count'),
    #     color=alt.Color('status:N', title='Status', scale=alt.Scale(scheme='tableau10')),
    #     width=600,
    #     height=300
    # ).configure_axis(
    #     grid=False
    # )   

    # Add a bar chart to visualize the success and failed API calls over time
    st.subheader("Comparison of Success")
    chart = alt.Chart(calls_per_day_rate).mark_bar().encode(
        x="date:T",
        y="success_calls_count:Q",
        color=alt.value("#2ecc71")
    ).properties(
        width=600,
        height=300
    )

    chart += alt.Chart(calls_per_day_rate).mark_bar().encode(
        x="date:T",
        y="failed_calls_count:Q",
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
