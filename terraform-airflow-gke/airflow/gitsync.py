from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import requests
import pandas as pd
import boto3
from io import BytesIO


def download_and_upload_to_minio():
    url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-01.parquet"
    response = requests.get(url)
    data = response.content
    df = pd.read_parquet(BytesIO(data))
    csv_data = df.to_csv(index=False).encode("utf-8")
    s3_client = boto3.client(
        "s3",
        endpoint_url="http://127.0.0.1:9000",
        aws_access_key_id="minioadmin",
        aws_secret_access_key="minioadmin",
    )

    s3_client.put_object(
        Bucket="airflow-minio", Key="nyc_data.csv", Body=BytesIO(csv_data)
    )


default_args = {
    "owner": "airflow",
    "start_date": datetime(2023, 1, 1),
    "retries": 1,
}

with DAG(
    "download_and_upload_to_minio", default_args=default_args, schedule_interval=None
) as dag:

    upload_task = PythonOperator(
        task_id="download_upload_nyc_data", python_callable=download_and_upload_to_minio
    )

upload_task
