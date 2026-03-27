import requests
import pandas as pd
import boto3
from datetime import datetime, timezone
from io import BytesIO

# ---------------------------
# CONFIG
# ---------------------------

BASE_URL = "https://api.eia.gov/v2/electricity/rto/daily-region-data/data/"
BUCKET = "energy-data-project-divjyot"

params = {
    "api_key": "13kegOaPuAQnnMd1yuGXU9oTFimL8SSNCvh4Ld6d",
    "frequency": "daily",
    "data[0]": "value",
    "sort[0][column]": "period",
    "sort[0][direction]": "desc",
    "offset": 0,
    "length": 5000
}

# ---------------------------
# INGEST
# ---------------------------

def fetch_data():
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

    return df

# ---------------------------
# VALIDATION
# ---------------------------

def validate_data(df):
    print("Shape:", df.shape)

    negatives = df[df["metric_value"] < 0]
    print("Negative values:", len(negatives))

    return df

# ---------------------------
# CLEANING (SILVER)
# ---------------------------

def clean_data(df):

    # remove redundant column
    if "timezone-description" in df.columns:
        df = df.drop("timezone-description", axis=1)

    # remove invalid negatives (Net generation only)
    df = df[~(
        (df["metric_name"] == "Net generation") &
        (df["metric_value"] < 0)
    )]

    # remove duplicates (safe even if none)
    df = df.drop_duplicates()
    
    df["metric_value"] = df["metric_value"].astype("float64")

    return df

# ---------------------------
# UPLOAD FUNCTION
# ---------------------------

def upload_to_s3(df, layer):

    s3 = boto3.client("s3")

    buffer = BytesIO()
    df.to_parquet(buffer, index=False)
    buffer.seek(0)

    now = datetime.now(timezone.utc)

    s3_key = f"{layer}/eia/year={now.year}/month={now.month}/day={now.day}/data.parquet"

    s3.put_object(
        Bucket=BUCKET,
        Key=s3_key,
        Body=buffer.getvalue()
    )

    print(f"{layer.upper()} upload successful:", s3_key)

# ---------------------------
# MAIN
# ---------------------------

def main():

    df = fetch_data()

    validate_data(df)

    # Bronze
    upload_to_s3(df, "bronze")

    # Silver
    df_clean = clean_data(df)
    upload_to_s3(df_clean, "silver")


# ---------------------------
# ENTRY
# ---------------------------

if __name__ == "__main__":
    main()