import snowflake.connector

conn = snowflake.connector.connect(
    user='sanjaykashyap',
    password='Bigdata@23',
    account='https://iogoldm-vcb38713.snowflakecomputing.com/',
    warehouse='COMPUTE_WH',
    database='SEVIR_META'
  #  schema=''
)

