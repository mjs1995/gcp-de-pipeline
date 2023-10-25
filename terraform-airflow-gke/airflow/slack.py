from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.slack.hooks.slack_webhook import SlackWebhookHook
from airflow.utils.dates import days_ago
from datetime import timedelta

def task_failure_callback(context):
    slack_msg = f"""
    :red_circle: Airflow Task Failed.
    *Task*: {context.get('task_instance').task_id}
    *Dag*: {context.get('task_instance').dag_id}
    *Execution Time*: {context.get('execution_date')}
    *Log Url*: {context.get('task_instance').log_url}
    """
    slack_hook = SlackWebhookHook(slack_webhook_conn_id='slack_webhook')
    slack_hook.send(text=slack_msg)

def task_success_callback(context):
    slack_msg = f"""
    :green_circle: Airflow Task Succeeded.
    *Task*: {context.get('task_instance').task_id}
    *Dag*: {context.get('task_instance').dag_id}
    *Execution Time*: {context.get('execution_date')}
    *Log Url*: {context.get('task_instance').log_url}
    """
    slack_hook = SlackWebhookHook(slack_webhook_conn_id='slack_webhook')
    slack_hook.send(text=slack_msg)

default_args = {
    'on_failure_callback': task_failure_callback,
    'start_date': days_ago(1)
}

with DAG(
    'slack_notification_dag',
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval=timedelta(days=1),
    catchup=False,
    tags=['example'],
) as dag:

    failure_task = DummyOperator(
        task_id='failure_task'
    )

    success_task = DummyOperator(
        task_id='success_task',
        on_success_callback=task_success_callback
    )

    failure_task >> success_task
