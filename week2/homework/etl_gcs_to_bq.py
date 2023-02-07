from pathlib import Path
import pandas as pd
import os
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials


@task(retries=3)
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read taxi data from web into pandas DataFrame"""
    df = pd.read_csv(dataset_url)
    return df


@task()
def write_local(df_clean: pd.DataFrame, color: str, dataset_file: str) -> Path:
    """Write Dataframe out as parquet file"""
    p = Path(f"data/{color}")
    p.mkdir(parents=True, exist_ok=True)
    file_name = f"{dataset_file}.parquet"
    file_path = p / file_name
    with file_path.open("w", encoding="utf-8") as f:
        df_clean.to_parquet(file_path, compression="gzip")
    
    return file_path


@task(retries=3)
def extract_from_gcs(color: str, year: int, month: int) -> Path:
    """Download trip data from GCS"""
    p = Path(f"data/{color}")
    p.mkdir(parents=True, exist_ok=True)
    gcs_path = f"data/{color}/{color}_tripdata_{year}-{month:02}.parquet"
    gcs_block = GcsBucket.load("gcs-bucket")
    gcs_block.get_directory(from_path=gcs_path, local_path=f"data")
    return Path(f"./data/{gcs_path}")


@task()
def write_gcs(path: Path) -> None:
    """Upload file to GCS"""
    gcp_block = GcsBucket.load("gcs-bucket")
    gcp_block.upload_from_path(from_path=path, to_path=path)
    return


@task()
def write_bq(path: Path) -> None:
    """Write to Big Query"""
    df = pd.read_parquet(path)
    gcp_credentials_block = GcpCredentials.load("gcp-creds")        
    df.to_gbq(destination_table='at_trips_data_all.homework', 
              project_id='de-nc-gr-pr-datateam', 
              credentials=gcp_credentials_block.get_credentials_from_service_account(), 
              chunksize=500000, 
              if_exists='append')


@flow()
def etl_gcs_to_bq(year: int, month: int, color: str):
    """Main ETL flow to load data into Big Query"""
    dataset_file = f"{color}_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz"
    df = fetch(dataset_url)
    path = write_local(df, color, dataset_file)
    write_gcs(path)
    path_gcs = extract_from_gcs(color, year, month)
    write_bq(path_gcs)


@flow()
def etl_parent_flow(months: list[int], year: int, color: str):
    for month in months:
        etl_gcs_to_bq(year, month, color)


if __name__ == '__main__':
    color = 'yellow'
    months = [2, 3]
    year = 2019
    etl_parent_flow(months, year, color)