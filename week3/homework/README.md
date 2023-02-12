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


## Question n.6

BigQuery supports a few external data sources: you may query these sources directly from BigQuery even though the data itself isn't stored in BQ.
An external table is a table that acts like a standard BQ table. The table metadata (such as the schema) is stored in BQ storage but the data itself is external.
In our case, data is store on GCP Bucket and we used the following command in order to create an external table starting from that data:

``` sql
CREATE OR REPLACE EXTERNAL TABLE `at_dataset.at_trips_data_all.homework3_external`
OPTIONS (
format = 'CSV',
uris = ['gs://at_data_lake_gcp/data/fhv/fhv_tripdata_2019-*.csv.gz']
);
```

## Question n.7

Clustering your data in BigQuery can improve query performance and reduce the cost of executing complex queries, but it's not always the best practice. Whether or not to cluster your data in BigQuery depends on your use case and specific requirements.

Here are a few factors to consider:

Query complexity: Clustering is most beneficial for complex queries that involve filtering and aggregating large amounts of data.

Query frequency: If you have a small number of infrequent complex queries, the benefits of clustering might not outweigh the cost of maintaining the clustered data.

Data size: Clustering is less effective for smaller datasets, as the overhead of creating and maintaining the cluster might outweigh the performance benefits.

Data distribution: Clustering is most effective when the data is distributed evenly across the clustering keys. If the data is skewed, clustering might not provide significant performance improvements.

In general, clustering is a useful technique for optimizing query performance in BigQuery, but it's important to carefully consider the trade-offs and weigh the benefits against the costs before deciding to implement it.