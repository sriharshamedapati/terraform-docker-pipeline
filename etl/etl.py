import os
import boto3
import pandas as pd
from io import StringIO

# ---- Config from ENV ----
AWS_ENDPOINT = os.getenv("AWS_ENDPOINT_URL")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID", "test")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "test")
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

RAW_PREFIX = "raw/input.csv"
PROCESSED_PREFIX = "processed/output.csv"

if not BUCKET_NAME or not AWS_ENDPOINT:
    raise Exception("Missing required environment variables")

# ---- S3 Client ----
s3 = boto3.client(
    "s3",
    endpoint_url=AWS_ENDPOINT,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name="us-east-1"
)

print("Connecting to S3...")
print(f"Bucket: {BUCKET_NAME}")

# ---- Extract ----
print("Downloading raw CSV...")
obj = s3.get_object(Bucket=BUCKET_NAME, Key=RAW_PREFIX)
data = obj["Body"].read().decode("utf-8")

df = pd.read_csv(StringIO(data))
print("Raw data loaded:")
print(df.head())

# ---- Transform ----
print("Transforming data...")
df = df[df[df.columns[0]].notna()]  # simple filter
df["row_length"] = df.apply(lambda x: len(str(x.tolist())), axis=1)

# ---- Load ----
csv_buffer = StringIO()
df.to_csv(csv_buffer, index=False)

s3.put_object(
    Bucket=BUCKET_NAME,
    Key=PROCESSED_PREFIX,
    Body=csv_buffer.getvalue()
)

print("ETL complete.")
print(f"Saved to s3://{BUCKET_NAME}/{PROCESSED_PREFIX}")
