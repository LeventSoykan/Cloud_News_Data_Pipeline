from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from cloud_spider import scrape_process

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'your_dag',
    default_args=default_args,
    description='Run Python script and dbt model weekly',
    schedule_interval=timedelta(weeks=1),
)

# Python script task
run_python_script = PythonOperator(
    task_id='run_python_script',
    python_callable=lambda: print("Running your_python_script.py"),
    dag=dag,
)

# dbt run task
run_dbt = BashOperator(
    task_id='run_dbt',
    bash_command='docker run --rm -v $(pwd):/dbt_project your_dbt_image_name',
    dag=dag,
)

# Set the task order
run_python_script >> run_dbt
