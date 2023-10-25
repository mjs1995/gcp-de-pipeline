import logging
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator
from airflow.utils.dates import days_ago
from datetime import datetime


def simple_python_task(**kwargs):
    logging.info("Executing Python Task!")
    return "Python Task executed successfully!"


dag = DAG(
    dag_id="slack_test",
    start_date=days_ago(1),
    max_active_runs=1,
    catchup=False,
    schedule_interval="@once",
)

python_task = PythonOperator(
    task_id="simple_python_task",
    python_callable=simple_python_task,
    provide_context=True,
    dag=dag,
)

slack_message_payload = {
    "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Hello, this is a *rich* slack message!",
            },
        },
        {
            "type": "image",
            "image_url": "https://github.com/mjs1995/diagrams/blob/2f26dbed7c63ee7a2f7817c9d00629cc89b96922/website/static/img/resources/onprem/analytics/pymy.png",
            "alt_text": "Example Image",
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Click Me"},
                    "value": "button_click",
                }
            ],
        },
    ]
}

send_rich_slack_message = SlackWebhookOperator(
    task_id="send_rich_slack_message",
    slack_webhook_conn_id="slack_webhook",
    message=slack_message_payload,
    dag=dag,
)

python_task >> send_rich_slack_message
