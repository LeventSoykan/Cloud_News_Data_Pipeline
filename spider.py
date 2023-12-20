import scrapy
import pandas as pd
from scrapy.crawler import CrawlerProcess


class NWSpider(scrapy.Spider):
    name = 'network_world_spider'
    def __init__(self):
        super().__init__()
        self.data = []

    def start_requests(self):
        urls = ['https://www.networkworld.com/cloud-computing/']
        for url in urls:
            yield scrapy.Request(url = url, callback = self.parse)

    def parse(self, response):
        file = 'scraped.csv'
        for a in response.xpath("//a[@class and contains(concat(' ', normalize-space(@class), ' '), ' card ')]"):  
            date = a.xpath('div[contains (@class, "card__info--light")]/span[1]/text()').extract()[0]
            if 'dec' in date.lower():
                self.data.append({
                    'name': a.xpath('h4/text()').extract()[0],
                    'link':a.xpath('@href').extract()[0],
                    'date':date
                })
        df = pd.DataFrame(self.data)
        df.to_csv(file, index=False)
        
        
if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(NWSpider)
    process.start()
