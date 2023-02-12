## Query n.1

``` sql
CREATE OR REPLACE EXTERNAL TABLE `at_dataset.at_trips_data_all.homework3_external`
OPTIONS (
format = 'CSV',
uris = ['gs://at_data_lake_gcp/data/fhv/fhv_tripdata_2019-*.csv.gz']
);


CREATE OR REPLACE TABLE `at_dataset.at_trips_data_all.homework3_internal` AS
SELECT * FROM `at_dataset.at_trips_data_all.homework3_external`;


SELECT count(*)
FROM `at_dataset.at_trips_data_all.homework3_internal`;
```
The result of the last query produces:
43244696

## Query n.2

``` sql
SELECT DISTINCT affiliated_base_number
FROM `at_dataset.at_trips_data_all.homework3_internal`;
```
This query will process 317.94 MB when run.

```
SELECT DISTINCT affiliated_base_number
FROM `at_dataset.at_trips_data_all.homework3_external`;
```
This query will process 0 B when run.

## Query n.3

``` sql
SELECT count(*) 
FROM `at_dataset.at_trips_data_all.homework3_internal`
WHERE PUlocationID IS NULL AND DOlocationID IS NULL
```

This result of the query is:
717748

## Query n.4

``` sql
CREATE OR REPLACE TABLE `at_dataset.at_trips_data_all.homework3_clustered`
PARTITION BY DATE(pickup_datetime)
CLUSTER BY affiliated_base_number AS
SELECT * FROM `at_dataset.at_trips_data_all.homework3_external`;
```

## Query n.5

``` sql
SELECT DISTINCT Affiliated_base_number FROM `at_dataset.at_trips_data_all.homework3_internal`
WHERE DATE(pickup_datetime) BETWEEN DATE(2019, 3, 1) AND DATE(2019, 3, 31);
```
This query will process 647.87 MB when run.

``` sql
SELECT DISTINCT Affiliated_base_number FROM `at_dataset.at_trips_data_all.homework3_clustered`
WHERE DATE(pickup_datetime) BETWEEN DATE(2019, 3, 1) AND DATE(2019, 3, 31);
```
This query will process 23.05 MB when run.
