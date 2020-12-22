import scrapy
import json


class ululespider(scrapy.Spider):
    name = "ulule"

    def start_requests(self):
        urls = [
            'https://www.ulule.com/195metres-film/',

        ]


    def parse(self, response):
        title=response.xpath('//title/text()').get()
