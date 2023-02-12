## Query n.1

``` sql
CREATE OR REPLACE EXTERNAL TABLE `de-nc-gr-pr-datateam.at_trips_data_all.homework3_external`
OPTIONS (
format = 'CSV',
uris = ['gs://at_data_lake_gcp_de-nc-gr-pr-datateam/data/fhv/fhv_tripdata_2019-*.csv.gz']
);


CREATE OR REPLACE TABLE `de-nc-gr-pr-datateam.at_trips_data_all.homework3_internal` AS
SELECT * FROM `de-nc-gr-pr-datateam.at_trips_data_all.homework3_external`;


SELECT count(*)
FROM `at_dataset.at_trips_data_all.homework3_internal`;
```

## Query n.2

``` sql
SELECT DISTINCT affiliated_base_number
FROM `at_dataset.at_trips_data_all.homework3_internal`;

SELECT DISTINCT affiliated_base_number
FROM `at_dataset.at_trips_data_all.homework3_external`;
```

## Query n.3

``` sql
SELECT count(*) 
FROM `at_dataset.at_trips_data_all.homework3_internal`
WHERE PUlocationID IS NULL AND DOlocationID IS NULL
```