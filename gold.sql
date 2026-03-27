CREATE DATABASE energy_db;

CREATE EXTERNAL TABLE silver_eia (
    date timestamp,
    region string,
    region_name string,
    metric_code string,
    metric_name string,
    metric_value double,
    ingestion_time timestamp
)
STORED AS PARQUET
LOCATION 's3://energy-data-project-divjyot/silver/eia/';

CREATE TABLE gold_energy_daily
WITH (
    external_location = 's3://energy-data-project-divjyot/gold/eia/',
    format = 'PARQUET'
) AS
SELECT 
    date,
    region,
    SUM(metric_value) AS total_energy
FROM silver
WHERE metric_name = 'Net generation'
GROUP BY date, region;