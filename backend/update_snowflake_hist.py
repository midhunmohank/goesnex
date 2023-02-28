import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import pandas as pd 

conn = snowflake.connector.connect(
    user='SANJAYKASHYAP',
    password='Bigdata@23',
    account='iogoldm-vcb38713',
    warehouse='COMPUTE_WH',
    database='SEVIR_META',
    schema='PUBLIC'
)

# df = pd.read_csv("goes_metadata.csv")


# df.columns = map(lambda x: str(x).upper(), df.columns)
# # print(df.head())

# success, nchunks, nrows, _ = write_pandas(conn, df, 'GOES')

# def get_hours(year, month, day):
#     cursor = conn.cursor()
    
#     cursor.execute("select hour from goes where day = ")
#     x = list(cursor.fetchall())
#     print(x)


# df = pd.read_csv("noes.csv")
# df.columns = map(lambda x: str(x).lower(), df.columns)
# print(df.head())
# success, nchunks, nrows, _ = write_pandas(conn, df, 'NOES')

# df = pd.read_excel("backend/nexrad.xlsx").dropna()
# df.columns = map(lambda x: str(x).upper(), df.columns)
# print(df.head())
# success, nchunks, nrows, _ = write_pandas(conn, df, 'NEXRAD_STATIONS')
