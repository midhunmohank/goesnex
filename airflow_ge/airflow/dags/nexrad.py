from airflow.models import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models.param import Param
from datetime import timedelta, datetime
import pandas as pd
import boto3
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas





# Load the environment variables from the .env file
load_dotenv()

# Set the base path
base_path = "/opt/airflow/working_dir"
# ge_root_dir = os.path.join(base_path, "great_expectations")
BASE_URL = os.getenv("DB_URL", "postgresql://root:root:root@db:5432/noaa")


def create_connection():
    conn = snowflake.connector.connect(
        user='SANJAYKASHYAP',
        password='Bigdata@23',
        account='iogoldm-vcb38713',
        warehouse='COMPUTE_WH',
        database='SEVIR_META',
        schema='PUBLIC'
    )
    return conn


# Set the S3 bucket name and prefix
bucket_name = "noaa-nexrad-level2"
prefix = "ABI-L1b-RadC/"
# s3 = boto3.resource("s3",)
s3 = boto3.client("s3", aws_access_key_id ="AKIAZW4EPXNKYZJXKP7Q", aws_secret_access_key="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" )

#check last updated date from snowflake
def check_last_updated_date_from_snowflake():
    # Create a cursor object
    conn = create_connection()
    cur = conn.cursor()
    query = """SELECT
                "year" AS latest_year,
                MAX("month") AS latest_month,
                MAX("day") AS latest_day
            FROM SEVIR_META.PUBLIC.NOES
            WHERE "year" = (
                SELECT MAX("year") FROM SEVIR_META.PUBLIC.NOES
            )
            GROUP BY "year";"""
    # Execute the SELECT statement to get the last N records from the table
    cur.execute(query)
    # Fetch the results as a list of tuples
    results = cur.fetchall()

    # Close the cursor and the database connection
    cur.close()
    conn.close()
    t = results[0]
    last_updated = datetime.strptime(f"{t[0]} {t[1]} {t[2]}", "%Y %j %H")
    return last_updated.strftime("%Y-%m-%d %H:%M:%S")

# get metadata and store
def get_metadata_and_store(s3, bucket_name, last_updated):
    last_updated = datetime.strptime(last_updated, "%Y-%m-%d %H:%M:%S")
    names = []
    #extract year from last_updated
    year = last_updated.year
    paginator = s3.meta.client.get_paginator("list_objects_v2")
    pages = paginator.paginate(Bucket=bucket_name,Prefix=str(year))
    # Loop through each page of objects
    for page in pages:
        for item in page['Contents']:
            names.append(item['Key'])
            # Parse the file name to get the year and day of year
            part = item['Key']
            parts = part.split("/")
            t = (int(parts[0]), int(parts[1]),int(parts[2]))
            file_date = datetime.strptime(f"{t[0]} {t[1]} {t[2]}", "%Y %j %H")

            # Check if the file is newer than the last updated date in Snowflake
            if file_date > last_updated:
                names.append(item['Key'])
    data = pd.DataFrame([i.split('/') for i in names], columns=['Year','Month','Day','Station_Name','File_Name'])
    data.drop('File_Name', axis=1, inplace=True)
    data.drop_duplicates(inplace=True)
    data_dicts = [row.to_dict() for _, row in data.iterrows()]
    return data_dicts

def write_to_snowflake(data_dicts):
    data = pd.DataFrame.from_records(data_dicts)
    try:
        conn = create_connection()
        data.columns = map(lambda x: str(x).upper(), data.columns)
        success, nchunks, nrows, _ = write_pandas(conn, data, 'NOES')
    except snowflake.connector.errors.DatabaseError as e:
        print("Error connecting to Snowflake database:", str(e))
    finally:
        conn.close()

dag = DAG(
    dag_id="nexrad",
    schedule= "0 0 * * *",
    start_date= days_ago(0),
    catchup=False,
    dagrun_timeout=timedelta(minutes=60),
    tags=["goes"]
)

with dag:
    check_last_updated_date_from_snowflake = PythonOperator(
        task_id="check_last_updated_date_from_snowflake",
        python_callable=check_last_updated_date_from_snowflake,
        dag=dag
    )

    get_metadata_and_store = PythonOperator(
        task_id="get_metadata_and_store",
        python_callable=get_metadata_and_store,
        op_kwargs={"s3": s3, "bucket_name": bucket_name, "last_updated": "{{ task_instance.xcom_pull(task_ids='check_last_updated_date_from_snowflake') }}"},
        dag=dag
    )

    write_to_snowflake = PythonOperator(
        task_id="write_to_snowflake",
        python_callable=write_to_snowflake,
        op_kwargs={"data_dicts": "{{ task_instance.xcom_pull(task_ids='get_metadata_and_store') }}"},
        dag=dag
    )

    check_last_updated_date_from_snowflake >> get_metadata_and_store >> write_to_snowflake