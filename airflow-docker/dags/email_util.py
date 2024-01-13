import os
import smtplib, ssl
import email.message
from datetime import datetime as dt
from sqlalchemy import create_engine
import pandas as pd
from airflow.models import Variable

def send_email():
    # Get data from Postgres DB
    #conn_url = os.environ.get('POSTGRES_CONNECTION_STRING')
    conn_url = Variable.get('POSTGRES_CONNECTION_STRING')
    engine = create_engine(f'{conn_url}cloudnewsdb', client_encoding='utf8')
    df = pd.read_sql('SELECT * FROM articles;', engine)

    # Create message
    sender = "leventsoykan@zohomail.eu"
    receiver = "levent_soykan@yahoo.com"
    m = email.message.Message()
    m['Subject'] = f'Cloud news for {dt.strftime(dt.today(), format="%Y-%m-%d")}'
    m['From'] = sender
    m['To'] = receiver
    m.add_header('Content-Type', 'text/html')
    m.set_payload(create_html(df), 'utf8')
    port = 587  # For SSL
    #email_user = os.environ.get('EMAIL_USER')
    #email_pass = os.environ.get('EMAIL_PASS')
    email_user = Variable.get('EMAIL_USER')
    email_pass = Variable.get('EMAIL_PASS')

    # Send email
    context = ssl.create_default_context()
    with smtplib.SMTP("smtp.zoho.eu", port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(email_user, email_pass)
        server.sendmail(sender, receiver, m.as_string())


def create_html(df):
    body = ''
    for _, row in df.iterrows():
        body += f"""
        <div style="border-style: solid; border-width: 3px; background-color: darkslategray;">
            <a style="display: block; height: 100%; width: 100%; text-decoration: none; color: white" href={row.iloc[1]}>
                {row.iloc[0]}
                <p>{row.iloc[3]}, {row.iloc[2]}</p>
            </a>
        </div>
        """
    html = f"""
        <head>
        <meta charset="UTF-8">
        <title>Cloud News</title>
    </head>
    <body>
        {body}
    </body>
    """
    return html

if __name__ == '__main__':
    send_email()