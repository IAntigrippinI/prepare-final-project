from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

# from service.hh import HHService
# from service.tg import TelegramService
# from service.analys import AnalysService

from config import settings
import loguru
from logger import *

from service import ParserService
from ml import Couch


def start(**context):
    loguru.logger.info("Start PARSING")
    ParserService().start_pipline()


def ml():
    loguru.logger.info("Start ML")
    Couch().fit()

#
# def analys():
#     AnalysService().start_analysis()


default_args = {
    "owner": "airflow",
    "retries": 0,
    "retry_delay": timedelta(seconds=15),
    # "on_failure_callback": send_failure_notification,
    # "on_retry_callback": send_failure_notification,
}

with DAG(
    dag_id="parse_nhl",
    default_args=default_args,
    description="Парсинг НХЛ",
    schedule_interval=timedelta(hours=24),
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["Parse"],
) as dag:

    t1 = PythonOperator(
        task_id="parsing_nhl_api",
        python_callable=start,
    )

    t2 = BashOperator(
        task_id="dbt_run",
        bash_command="dbt run",
        cwd="/opt/airflow/kbi_project",
    )

    t3 = PythonOperator(
        task_id="ml_train",
        python_callable=ml,
    )


    t1 >> t2 >> t3