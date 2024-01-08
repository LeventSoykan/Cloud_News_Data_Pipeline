from datetime import datetime as dt
import scrapy
import pandas as pd
from sqlalchemy import create_engine
from scrapy.crawler import CrawlerProcess
import os

class NWSpider(scrapy.Spider):
    name = 'network_world_spider'
    def __init__(self):
        super().__init__()
        conn_url = os.environ.get('POSTGRES_CONNECTION_STRING')
        self.engine = create_engine(f'{conn_url}cloudnewsdb')
        self.data = []

    def start_requests(self):
        urls = ['https://www.networkworld.com/cloud-computing/']
        for url in urls:
            yield scrapy.Request(url = url, callback = self.parse)

    def parse(self, response):
        for a in response.xpath("//a[@class and contains(concat(' ', normalize-space(@class), ' '), ' card ')]"):
            date = a.xpath('div[contains (@class, "card__info--light")]/span[1]/text()').extract()[0]
            if 'dec' in date.lower():
                self.data.append({
                    'title': a.xpath('h4/text()').extract()[0],
                    'url':a.xpath('@href').extract()[0],
                    'date':date,
                    'source': 'Network World',
                    'query_date': dt.now()
                })
        df = pd.DataFrame(self.data)
        df.to_sql('raw', self.engine, if_exists='replace')


def scrape_process():
    print('Python process start tested')
    #process = CrawlerProcess()
    #process.crawl(NWSpider)
    #process.start()


if __name__ == '__main__':
    scrape_process()
