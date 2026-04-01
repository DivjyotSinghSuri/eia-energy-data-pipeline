# EIA Energy Data Pipeline

## Overview

This project implements an end-to-end data pipeline that ingests energy data from the U.S. Energy Information Administration (EIA) API, processes it, and stores it in AWS S3 using a medallion architecture (Bronze → Silver).

The pipeline is designed to be reproducible, structured, and analytics-ready, with partitioned storage and clean transformation logic.

---

## Architecture

- **Ingestion & Processing**: Python (requests, pandas)
- **Storage**: AWS S3 (Bronze & Silver layers)
- **Format**: Parquet
- **Partitioning**: Year / Month / Day
- **Planned Query Layer**: AWS Athena / SQL-based analytics

---

## Data Flow

1. Fetch energy data from EIA API
2. Convert raw response into structured DataFrame
3. Perform basic validation (nulls, type checks, anomalies)
4. Store raw data in S3 (**Bronze layer**)
5. Apply cleaning logic:
   - Remove invalid negative values (Net generation)
   - Drop redundant columns
   - Ensure consistent schema
6. Store cleaned data in S3 (**Silver layer**)

---

## Tech Stack

- Python  
- Pandas  
- Boto3  
- AWS S3  
- Parquet  

---

## Current Status

- ✅ API ingestion pipeline implemented  
- ✅ Bronze layer (raw data) stored in S3  
- ✅ Silver layer (cleaned data) stored in S3  
- ⏳ Gold layer (analytical queries) planned using SQL  

---

## Future Improvements

- Implement Gold layer using SQL (Athena or DuckDB)
- Add analytical use cases:
  - Regional energy production trends  
  - Import vs export dependency analysis  
  - Peak energy usage detection  
- Introduce workflow orchestration (Airflow / cron)
- Add monitoring and validation checks
- Build dashboard for visualization

---

## How to Run

1. Configure AWS CLI:

   ```bash
   aws configure
   
2. Install dependencies:

   ```bash
   pip install boto3 pandas requests pyarrow

3. Run the pipeline:

   ```python
   eia_pipeline.py
