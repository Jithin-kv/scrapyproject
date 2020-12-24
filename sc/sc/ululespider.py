import scrapy
import re
import json
from scrapy.http import Request, FormRequest
from scrapy.spiders import Spider
#from sc.items import *
#from sc.settings import *



headers={
'authority': 'www.ulule.com',
'method':'GET',
'path': '/ 195metres - film /',
'scheme':'https',
'accept':'text / html,application / xhtml + xml, application / xml;,q = 0.9, image / avif, image / webp, image / apng, * / *;q = 0.8, application / signed - exchange;,v= b3;,q= 0.9',
'accept - encoding': 'gzip, deflate, br',
'accept - language':'en - GB, en - US;,q = 0.9, en;q = 0.8',
'cache - control': 'max - age = 0',
'sec - fetch - dest': 'document',
'sec - fetch - mode': 'navigate',
'sec - fetch - site': 'none',
'sec - fetch - user': '?1',
'upgrade - insecure - requests': '1',
'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'

}



class ululespider(scrapy.Spider):
    name = "ulule"

    def start_requests(self):
        start_urls = ['https://www.ulule.com/195metres-film/']


    def parse(self, response):
        json_data = response.xpath('//script[contains(text(),"project: {")]/text()').extract_first('').strip()

        name = response.xpath('//meta[@property="og:title"]/@content').extract_first()
        short_description = response.xpath('//meta[@property="og:description"]/@content').extract_first()
        no_of_supporters = re.findall(r'"supporters_count": (\d+)', json_data)
        fund_raised ={}
        amount=re.findall(r'"amount_raised": (\d+)', json_data)[0]
        currency=re.findall(r'"currency".*?",',json_data)
        goal = re.findall(r'"goal": (\d+)', json_data)
        percentage_funded = re.findall(r'"percent": (\d+)', json_data)
        days_left=re.findall(r'"comments_count":(\d+)',json_data)

        cu = re.findall(r'"currency".*?",', json_data)[0].strip(',').strip('"')
        currency = cu.strip('currency": "')
        fund={
            'amount':amount,
	       'currency':currency
             }
        fund_raised.update(fund)
