# EIA Energy Data Pipeline

## Overview

This project builds an end-to-end data pipeline that ingests energy data from the EIA API, stores it in AWS S3, and prepares it for analytics using a medallion architecture (Bronze → Silver → Gold).

## Architecture

* **Ingestion**: Python script (requests, pandas, boto3)
* **Storage**: AWS S3 (Bronze layer)
* **Processing**: Databricks (planned Silver & Gold layers)
* **Format**: Parquet
* **Partitioning**: Year / Month / Day

## Data Flow

1. Fetch data from EIA API
2. Transform into structured DataFrame
3. Validate basic data quality (nulls, duplicates)
4. Store in S3 (Bronze layer)
5. Process in Databricks (Silver & Gold layers)

## Tech Stack

* Python
* Pandas
* Boto3
* AWS S3
* Databricks
* Parquet

## Current Status

* ✅ API ingestion complete
* ✅ Data stored in S3 (partitioned)
* ⏳ Silver layer (cleaning & validation) in progress
* ⏳ Gold layer (analytics) planned

## Future Improvements

* Add automated scheduling (cron / Airflow)
* Implement data validation checks
* Build analytics layer (daily trends, peak demand)
* Add dashboard for visualization

## How to Run

1. Configure AWS CLI
2. Install dependencies:

   ```
   pip install boto3 pandas requests pyarrow
   ```
3. Run:

   ```
   python api_ingestion.py
   ```

## Key Learnings

* Building data ingestion pipelines using APIs
* Handling cloud storage (S3)
* Data partitioning and storage formats
* Structuring pipelines using medallion architecture
