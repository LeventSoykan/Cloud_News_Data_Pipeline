FROM python:3.8

WORKDIR /dbt

COPY ./dbt/cloudnews .

RUN pip install --upgrade pip
RUN pip install dbt-postgres

CMD ["dbt", "run"]