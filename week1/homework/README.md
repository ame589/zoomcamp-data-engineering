# Homework week 1


This repository contains a docker-compose.yml file for setting up a multi-container application.
Prerequisites

    Docker
    Docker Compose
    Jupyter Notebook

Usage

    Clone this repository to your local machine:

git clone [https://github.com/ame589/zoomcamp-data-engineering.git](https://github.com/ame589/zoomcamp-data-engineering.git)

    Navigate to the repository directory:

cd <repo>

    Build and start the containers using docker-compose:

docker volume create --name dtc_postgres_volume_local -d local

    Create a local volume

docker-compose up --build

    To stop the containers, use the following command:

docker-compose down

Services

This docker-compose.yml file defines the following services:

    pg-database: This service runs the postgres:13 container, and exposes port 5432.

You can add more services to the docker-compose.yml file as per your need.
Volumes

This docker-compose.yml file also defines the following volumes:

    dtc_postgres_volume_local: This volume is used by the pg-database to persist data.

You can add more volumes to the docker-compose.yml file as per your need.
- The file [upload-data-green-taxi.ipynb](upload-data-green-taxi.ipynb) is a jupyter script responsible to ingest green taxi data downloaded from https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz into a local Postgres instance.
- The file [upload-data-zones.ipynb](upload-data-zones.ipynb) is a jupyter script responsible to ingest zones data downloaded from https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv into a local Postgres instance.


Exercises solutions:

1. docker build --help
2. Execute the following commands:
   1. docker run -it --entrypoint=bash python:3.9
   2. pip list
3. Go to [upload-data-green-taxi.ipynb](upload-data-green-taxi.ipynb) and [upload-data-zones.ipynb](upload-data-zones.ipynb)
## Query n.3

``` sql
SELECT count(*)
FROM green_taxi_data
WHERE lpep_pickup_datetime::date = date '2019-01-15' AND lpep_dropoff_datetime::date = date '2019-01-15';
```
## Query n.4

``` sql
SELECT lpep_pickup_datetime::date, trip_distance
FROM green_taxi_data
ORDER BY trip_distance DESC
LIMIT 1;
```
## Query n.5

``` sql
SELECT count(*), '2_PASSENGERS'
FROM green_taxi_data
WHERE lpep_pickup_datetime::date = date '2019-01-01' AND passenger_count = 2
UNION ALL
SELECT count(*), '3_PASSENGERS'
FROM green_taxi_data
WHERE lpep_pickup_datetime::date = date '2019-01-01' AND passenger_count = 3;
```
## Query n.6

``` sql
SELECT "Zone"
FROM taxi_zone
WHERE "LocationID" = 
(
    SELECT t."DOLocationID"
    FROM green_taxi_data t
    JOIN taxi_zone tz
        ON t."PULocationID" = tz."LocationID"
    WHERE tz."Zone" = 'Astoria'
    ORDER BY t."tip_amount" DESC
    LIMIT 1
);
```
