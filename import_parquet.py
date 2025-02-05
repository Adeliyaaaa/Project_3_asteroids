import pandas as pd
from sqlalchemy import create_engine
import time
import os 
from dotenv import load_dotenv
load_dotenv()

df = pd.read_parquet("df_asteroides_partial1.parquet") # read csv file from your local

dbname = os.getenv("dbname")
user = os.getenv("user")
password = os.getenv("password")
host = os.getenv("host")
port = os.getenv("port")

# Example: 'postgresql://username:password@localhost:5432/your_database'
engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{dbname}')

#postgresql://<user>:<password>@<host>:<port>/<database>

start_time = time.time() # get start time before insert

df.to_sql(
    name="asteroids1", # table name
    con=engine,  # engine
    if_exists="replace", #  If the table already exists, append or replace
    index=False # no index
)

end_time = time.time() # get end time after insert
total_time = end_time - start_time # calculate the time
print(f"Insert time: {total_time} seconds") # print time