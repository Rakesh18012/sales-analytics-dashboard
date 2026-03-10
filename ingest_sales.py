"""
ingest_sales.py
Pulls sales data from REST API and CSV files → cleans → loads to Amazon S3.
Runs daily via Airflow DAG before dbt transformations kick in.
"""

import pandas as pd
import boto3
import requests
import logging
import os
from datetime import datetime, timedelta
from io import StringIO

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

S3_BUCKET = os.environ.get("S3_BUCKET", "sales-data-lake")
API_BASE  = os.environ.get("SALES_API_URL", "https://api.salesplatform.com/v1")
API_KEY   = os.environ.get("SALES_API_KEY", "")


def fetch_orders_from_api(start_date: str, end_date: str) -> pd.DataFrame:
    """Fetch orders from Sales REST API with pagination."""
    logger.info(f"Fetching orders from {start_date} to {end_date}")
    all_orders, page = [], 1

    while True:
        resp = requests.get(
            f"{API_BASE}/orders",
            headers={"Authorization": f"Bearer {API_KEY}"},
            params={"start_date": start_date, "end_date": end_date, "page": page, "limit": 500},
            timeout=30
        )
        data = resp.json()
        if not data.get("orders"):
            break
        all_orders.extend(data["orders"])
        page += 1
        logger.info(f"  Page {page-1}: {len(data['orders'])} orders")

    df = pd.DataFrame(all_orders)
    logger.info(f"Total orders fetched: {len(df):,}")
    return df


def clean_orders(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize orders dataframe."""
    df = df.dropna(subset=["order_id", "customer_id", "order_date"])
    df["order_date"]    = pd.to_datetime(df["order_date"])
    df["order_amount"]  = pd.to_numeric(df["order_amount"], errors="coerce").fillna(0)
    df["product_id"]    = df["product_id"].astype(str).str.strip()
    df["customer_id"]   = df["customer_id"].astype(str).str.strip()
    df["region"]        = df["region"].str.upper().fillna("UNKNOWN")
    df["ingested_at"]   = datetime.now()
    df = df.drop_duplicates(subset="order_id")
    logger.info(f"Clean orders: {len(df):,} rows")
    return df


def upload_to_s3(df: pd.DataFrame, prefix: str):
    """Upload DataFrame as Parquet to S3."""
    s3 = boto3.client("s3")
    date_str = datetime.now().strftime("%Y/%m/%d")
    key = f"{prefix}/{date_str}/data.parquet"

    buffer = df.to_parquet(index=False)
    s3.put_object(Bucket=S3_BUCKET, Key=key, Body=buffer)
    logger.info(f"Uploaded {len(df):,} rows to s3://{S3_BUCKET}/{key}")
    return f"s3://{S3_BUCKET}/{key}"


def run_ingestion():
    end_date   = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    # Orders
    orders_df = fetch_orders_from_api(start_date, end_date)
    orders_df = clean_orders(orders_df)
    upload_to_s3(orders_df, "raw/orders")

    logger.info("Ingestion complete!")


if __name__ == "__main__":
    run_ingestion()
