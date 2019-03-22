#/home/safir/anaconda3/bin/python
# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess


class AliexpressTabletsSpider(scrapy.Spider):
    name = 'aliexpress_tablets'
    #allowed_domains = ['https://www.aliexpress.com/category/200216607/tablet.html']
    allowed_domains = ['aliexpress.com']
    start_urls = ['https://www.aliexpress.com/category/200216607/tablet.html']

    custom_settings = { 'FEED_FORMAT': 'csv',
                        'FEED_URI': '/home/safir/Desktop/scrapy-learning/aliexpress/aliexpress/spiders/aliexpress_%(time)s.csv' }

    def parse(self, response):
        print("Processing", response.url)

        product_name = response.xpath("//div/h3/a/text()").extract()
        price_range = response.xpath("//div//span[@class='value']/text()").extract()
        orders = response.xpath("//div[@class='rate-history']/span[@rel='nofollow']//em/text()").extract()
        company_name = response.xpath("//div[@class='info-more']//a/text()").extract()

        row_data = zip(product_name, price_range, orders, company_name)

        for item in row_data:

            scraped_info = {
                'page': response.url,
                'product_name': item[0],
                'price_range': item[1],
                'orders': item[2],
                'company_name': item[3],
            }

            yield scraped_info

        next_page = response.xpath("//div[@class='ui-pagination-navi util-left']/a/@href").extract_first()

        if next_page:
            yield scrapy.Request(response.urljoin(next_page),
                                 callback=self.parse)



process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(AliexpressTabletsSpider)
process.start() # the script will block here until the crawling is finished