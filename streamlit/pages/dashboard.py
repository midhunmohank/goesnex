import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from datetime import datetime, timedelta
import base64
import requests
import json

api_host = "http://localhost:8000"
access_token = st.session_state["access_token"]
headers = {"Authorization": f"Bearer {access_token}"}
# Get today's date
today = datetime.today()

# Calculate yesterday's date
yesterday = today - timedelta(days=1)

# Dummy data for user countAPI 
activity_data = {
    "user1": {"2022-01-01": 10, "2022-01-02": 15, "2022-01-03": 12},
    "user2": {"2022-01-01": 8, "2022-01-02": 20, "2022-01-03": 7},
    "user3": {"2022-01-01": 5, "2022-01-02": 14, "2022-01-03": 18}
}

# Create a dummy data for total API calls
total_api_calls_data = pd.DataFrame({
    'date': pd.date_range(datetime.today() - timedelta(days=8), periods=8),
    'total_api_calls': np.random.randint(low=100, high=200, size=(8,))
})

# Dummy data for API request calls
api_calls_data = pd.DataFrame({
    'date': pd.date_range(datetime.today() - timedelta(days=8), periods=8),
    'success_calls': np.random.randint(low=50, high=150, size=(8,)),
    'failed_calls': np.random.randint(low=0, high=50, size=(8,))
})


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



# Define the Streamlit app
def app():
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
        chart_data = total_api_calls_data
        chart = alt.Chart(chart_data).mark_line().encode(
            x='date:T',
            y='total_api_calls:Q'
        )
        st.altair_chart(chart)

    # Add a table to show the user activity data
    st.subheader("User Activity Data")
    st.dataframe(df)
    # Add a stacked bar chart to visualize successful and failed API request calls
    chart_data = api_calls_data.set_index('date').stack().reset_index().rename(columns={'level_1': 'status', 0: 'count'})
    chart_data['status'] = chart_data['status'].str.replace('_calls', '').str.title()

    chart = alt.Chart(chart_data).mark_bar().encode(
        x=alt.X('date:T', title='Date'),
        y=alt.Y('sum(count):Q', title='Count'),
        color=alt.Color('status:N', title='Status', scale=alt.Scale(scheme='tableau10')),
        width=600,
        height=300
    ).configure_axis(
        grid=False
    )   

    # Add a bar chart to visualize the success and failed API calls over time
    st.subheader("Comparison of Success")
    chart = alt.Chart(api_calls_data).mark_bar().encode(
        x="date:T",
        y="success_calls:Q",
        color=alt.value("#2ecc71")
    ).properties(
        width=600,
        height=300
    )

    chart += alt.Chart(api_calls_data).mark_bar().encode(
        x="date:T",
        y="failed_calls:Q",
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
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="user_activity.csv">Download User Activity Data (CSV)</a>'
    st.markdown(href, unsafe_allow_html=True)

    csv = total_api_calls_data.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="total_api_calls.csv">Download Total API Calls Data (CSV)</a>'
    st.markdown(href, unsafe_allow_html=True)

    st.write("---")
    st.write(f"Dashboard last updated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")

app()
