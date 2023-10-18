from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

def print_hello():
    print("Hello, Airflow!")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'hello_airflow',
    description='Simple tutorial DAG',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 10, 17),
    catchup=False,
    default_args=default_args
)

t1 = PythonOperator(
    task_id='print_hello',
    python_callable=print_hello,
    dag=dag
)

t1