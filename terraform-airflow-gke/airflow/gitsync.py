from airflow import DAG
from airflow.hooks.base_hook import BaseHook
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import requests
import pandas as pd
import boto3
import json
from io import BytesIO


def download_and_upload_to_minio():
    url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-01.parquet"
    response = requests.get(url)
    data = response.content
    df = pd.read_parquet(BytesIO(data))
    csv_data = df.to_csv(index=False).encode("utf-8")
    conn = BaseHook.get_connection("minio-test")
    extra_config = json.loads(conn.extra)

    s3_client = boto3.client(
        "s3",
        endpoint_url=extra_config["host"],
        aws_access_key_id=conn.login,
        aws_secret_access_key=conn.password,
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
