from pathlib import Path
import os
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket


@task(retries=3)
def fetch(dataset_url: str, dataset_file: str) -> Path:
    """Read taxi data from web into pandas DataFrame"""
    p = Path(f"data/fhv/")
    p.mkdir(parents=True, exist_ok=True)
    file_name = f"{dataset_file}.csv.gz"
    file_path = p / file_name
    os.system(f"wget {dataset_url} -O data/fhv/{file_name}")
    return file_path


@task()
def write_gcs(path: Path) -> None:
    """Upload file to GCS"""
    gcp_block = GcsBucket.load("gcs-bucket")
    gcp_block.upload_from_path(from_path=path, to_path=path)
    return

@flow()
def etl_web_to_gcs(month: int, year: int) -> None:
    """The main ETL function"""
    dataset_file = f"fhv_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/{dataset_file}.csv.gz"
    path = fetch(dataset_url, dataset_file)
    write_gcs(path)


@flow()
def etl_parent_flow(months: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], year: int = 2019):
    for month in months:
        etl_web_to_gcs(month, year)


if __name__ == '__main__':
    months: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    year: int = 2019
    etl_parent_flow(months, year)
