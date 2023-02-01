from pathlib import Path
import pandas as pd
import os
from datetime import timedelta
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect.tasks import task_input_hash


@task(retries=3, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read taxi data from web into pandas DataFrame"""
    df = pd.read_csv(dataset_url)
    return df

@task(log_prints=True)
def clean(df: pd.DataFrame) -> pd.DataFrame:
    """fix dtype issues"""
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
    print(df.head(2))
    print(f"columns: {df.dtypes}")
    print(f"rows: {len(df)}")
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


@task()
def write_gcs(path: Path) -> None:
    """Upload file to GCS"""
    gcp_block = GcsBucket.load("gcs-bucket")
    gcp_block.upload_from_path(from_path=path, to_path=path)
    return

@flow()
def etl_web_to_gcs(year: int, month: int, color: str) -> None:
    """The main ETL function"""
    dataset_file = f"{color}_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz"

    df = fetch(dataset_url)
    df_clean = clean(df)
    path = write_local(df_clean, color, dataset_file)
    write_gcs(path)


@flow()
def etl_parent_flow(months: list[int] = [1, 2], year: int = 2021, color: str = "yellow"):
    for month in months:
        etl_web_to_gcs(year, month, color)


if __name__ == '__main__':
    color = 'yellow'
    month = [1, 2, 3]
    year = 2021
    etl_parent_flow(month, year, color)