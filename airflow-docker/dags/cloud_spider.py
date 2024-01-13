from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime as dt
from sqlalchemy import create_engine
import os
from urllib.request import Request, urlopen
from airflow.models import Variable

class CloudSpider():
    def __init__(self):
        conn_url = Variable.get('POSTGRES_CONNECTION_STRING')
        #conn_url = os.environ.get('POSTGRES_CONNECTION_STRING')
        self.engine = create_engine(f'{conn_url}cloudnewsdb')
        self.data = []
    
    @staticmethod
    def get_soup(url):
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        page = urlopen(req).read()
        soup = BeautifulSoup(page, 'lxml')
        return soup

    def extract_nw(self):
        soup = self.get_soup('https://www.networkworld.com/cloud-computing/')
        for a in soup.find_all('a', attrs={'class': 'card'}):
            date = a.find_next('div', attrs={'class': 'card__info--light'}).find_next('span').text
            self.data.append({
                'title': a.find_next('h4').text,
                'url': a['href'],
                'date': date,
                'source': 'Network World',
                'query_date': dt.now()
            })
                
    def extract_cd(self):
        soup = self.get_soup('https://www.ciodive.com/topic/cloud/')
        for li in soup.select('li.row.feed__item'):
            a = li.find_next('h3', attrs={'class': 'feed__title'}).find_next('a')
            url = 'https://www.ciodive.com/' + a['href']
            title = a.text.strip()
            try:
                date = li.find_all('span', attrs={'class':'secondary-label'})[1].text
            except:
                pass
            self.data.append({
            'title':title,
            'url': url,
            'date': date.replace('.',''),
            'source': 'Ciodive',
            'query_date': dt.now()
            })
            
    def extract_cc(self):
        soup = self.get_soup('https://www.cloudcomputing-news.net/categories/cloud-computing/')
        for article in soup.find_all('article', attrs={'class':'archive-post'}):
            a =  article.find_next('header').find_next('a')
            byline = article.find_next('div', attrs={'class':'byline'})
            self.data.append({
            'title':a.text.strip(),
            'url': a['href'],
            'date': byline.text.split('|')[0].strip(),
            'source': 'Cloudtech',
            'query_date': dt.now()
            })
            
    def process_extraction(self):
        self.extract_nw()
        self.extract_cd()
        self.extract_cc()
            
    def get_df(self):
        return pd.DataFrame(self.data)

    def update_sql(self):            
        df = pd.DataFrame(self.data)
        df.to_sql('raw', self.engine, if_exists='replace')

        
def data_extraction():
    spider = CloudSpider()
    spider.process_extraction()
    spider.update_sql()

if __name__ == '__main__':
    data_extraction()
