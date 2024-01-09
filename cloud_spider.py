from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime as dt
from sqlalchemy import create_engine
import os

class NWSpider():
    def __init__(self, url):
        conn_url = os.environ.get('POSTGRES_CONNECTION_STRING')
        self.engine = create_engine(f'{conn_url}cloudnewsdb')
        self.data = []
        self.url = url

        source = requests.get(url).text
        self.soup = BeautifulSoup(source, 'lxml')

    def extract(self):
        for a in self.soup.find_all('a', attrs={'class': 'card'}):
            date = a.find_next('div', attrs={'class': 'card__info--light'}).find_next('span').text
            if 'dec' in date.lower():
                print()
                print()
                self.data.append({
                    'title': a.find_next('h4').text,
                    'url': a['href'],
                    'date': date,
                    'source': 'Network World',
                    'query_date': dt.now()
                })
        df = pd.DataFrame(self.data)
        df.to_sql('raw', self.engine, if_exists='replace')

if __name__ == '__main__':
    spider = NWSpider('https://www.networkworld.com/cloud-computing/')
    spider.extract()
