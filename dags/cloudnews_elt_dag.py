from airflow import DAG
from airflow.operators.python_operator import PythonOperator, PythonVirtualenvOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from cloud_spider import scrape_process

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 6),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'cloudnews_elt_dag',
    default_args=default_args,
    description='Run Python script and dbt model weekly',
    schedule_interval=timedelta(weeks=1),
)

# Python script task
run_python_script = PythonVirtualenvOperator(
    task_id='run_spider',
    requirements='scrapy',
    python_callable=scrape_process,
    dag=dag,
)

# dbt run task
run_dbt = BashOperator(
    task_id='run_dbt',
    bash_command='dbt run --project-dir dbt/',
    dag=dag,
)

# Set the task order
run_python_script >> run_dbt
