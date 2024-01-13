# Cloud News Data Pipeline

![GitHub stars](https://img.shields.io/github/stars/LeventSoykan/Cloud_News_Data_Pipeline?style=flat-square)
![GitHub forks](https://img.shields.io/github/forks/LeventSoykan/Cloud_News_Data_Pipeline?style=flat-square)
![GitHub license](https://img.shields.io/github/license/LeventSoykan/Cloud_News_Data_Pipeline?style=flat-square)

A data pipeline for collecting and processing cloud-related news articles. This project aims to provide a systematic way to aggregate news articles related to cloud computing from various sources and transform them into a structured dataset for analysis.

## Table of Contents

- [Introduction](#introduction)
- [ELT](#elt)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [License](#license)

## Introduction

In the fast-evolving field of cloud computing, staying up-to-date with the latest news is crucial. This project offers a solution for creating a data pipeline to automate the collection, processing, and storage of cloud-related news articles. 
The pipeline utilizes various technologies to ensure efficiency and reliability in managing this data. 

## ELT

- **Data Extraction:** Automatically fetches cloud-related news articles from specified sources using Python Beautifulsoup and Pandas library. (airflow-docker/dags/cloud_spider.py)
- **Data Loading:** Data is loaded to a Postgresql Database on a remote server as raw table, using SQLAlchemy (airflow-docker/dags/cloud_spider.py)
- **Data Transformation:** Data types, colunm names are transformed, data is ordered and filtered by a DBT project (dbt/cloudnews/models/cloudnews/articles.sql)
- **Send the cloud articles in email:** An email is  (airflow-docker/dags/email_util.py)
- **Scheduled to run weekly:** An Airflow dag is prepared to run these processes weekly. Both DBT and Airflow run on docker on remote linux server. 

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed
- Remote server with Docker installed
- Access to a Postgresql database for storing the raw and processed data (e.g., MongoDB, MySQL)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/LeventSoykan/Cloud_News_Data_Pipeline.git
    ```
2. Build the docker image from dbt folder with the name dbt docker:

    ```bash
    docker build -t dbt-docker .
    ```
    **Note that the variables for DB and email user should be updated in Airflow
3. Build and run the docker image from airflow-docker directory:

    ```bash
    docker-compose up airflow-init
    ```
   Then run the airflow container
   
    ```bash
    docker compose up
    ```
    
## License

This project is licensed under the [MIT License](LICENSE).
