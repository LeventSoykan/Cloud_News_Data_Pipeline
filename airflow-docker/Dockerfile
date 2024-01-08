FROM apache/airflow:2.8.0
COPY requirements.txt /requirements.txt
RUN pip install --user --upgrade pip
RUN pip install Scrapy
RUN pip install dbt-postgres
RUN pip install dbt-core
