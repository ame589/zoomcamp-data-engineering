import pandas as pd
import argparse
import os
from sqlalchemy import create_engine
from time import time


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    parquet_name = 'output.parquet'
    csv_name = 'output.csv'

    # download the parquet file
    os.system(f"wget {url} -O {parquet_name}")
    
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df_parquet = pd.read_parquet(f'/app/{parquet_name}')
    df_parquet.to_csv(f'/app/{csv_name}')
    df_iter = pd.read_csv(f'/app/{csv_name}', iterator=True, chunksize=100000)

    df = next(df_iter)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    df.to_sql(name=table_name, con=engine, if_exists='append')

    while True:
        t_start = time()
        df = next(df_iter)
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
        df.to_sql(name=table_name, con=engine, if_exists='append')
        t_end = time()
        print('inserted another chunk, took %.3f second' % (t_end - t_start))
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Ingest CSV data to Postgres')

    parser.add_argument('--user', help='user name for postgres')           
    parser.add_argument('--password', help='password for postgres')      
    parser.add_argument('--host', help='host name for postgres')  
    parser.add_argument('--port', help='port name for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='name of the table where we will write the results to')
    parser.add_argument('--url', help='url of the csv file')

    args = parser.parse_args()
    main(args)