import requests
import pandas as pd
import boto3
from datetime import datetime, timezone
from io import BytesIO

BASE_URL = "https://api.eia.gov/v2/electricity/rto/daily-region-data/data/"

params = {
    "api_key": "YOUR_API_KEY",
    "frequency": "daily",
    "data[0]": "value",
    "sort[0][column]": "period",
    "sort[0][direction]": "desc",
    "offset": 0,
    "length": 5000
}


response = requests.get(BASE_URL, params=params)

if response.status_code != 200:
    raise Exception("API failed")

data = response.json()
records = data["response"]["data"]

df = pd.DataFrame(records)

df["value"] = pd.to_numeric(df["value"], errors="coerce")
df["period"] = pd.to_datetime(df["period"])
df["ingestion_time"] = datetime.now(timezone.utc)

df.rename(columns={
    "period": "date",
    "respondent": "region",
    "respondent-name": "region_name",
    "type": "metric_code",
    "type-name": "metric_name",
    "value": "metric_value"
}, inplace=True)


df.to_parquet("energy_data.parquet", index=False)

now = datetime.now(timezone.utc)
s3 = boto3.client("s3")

s3_key = f"bronze/eia/year={now.year}/month={now.month}/day={now.day}/energy_data.parquet"

s3.upload_file(
    "energy_data.parquet",
    "energy-data-project-divjyot",
    s3_key)


print("Upload successful:", s3_key)