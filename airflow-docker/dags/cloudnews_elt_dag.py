from airflow import DAG
from airflow.operators.python_operator import PythonOperator, PythonVirtualenvOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.docker_operator import DockerOperator
from datetime import datetime, timedelta
from cloud_spider import data_extraction
from email_util import send_email

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
run_python_script = PythonOperator(
    task_id='run_spider',
    python_callable=data_extraction,
    dag=dag,
)

# dbt run task
run_dbt = DockerOperator(
    task_id='run_dbt',
    image='dbt-docker',
    api_version='auto',
    auto_remove=True,
    #command='dbt run',
    docker_url='unix://var/run/docker.sock',
    network_mode='bridge'
)

# Email task
send_email = PythonOperator(
    task_id='send_email',
    python_callable=send_email,
    dag=dag,
)

# Set the task order
run_python_script >> run_dbt >> send_email
