# -*- coding: utf-8 -*-
import scrapy
import re
import json
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest
from ulul.items import *




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




class UluleSpider(scrapy.Spider):
    name = 'ulule'
    allowed_domains = []
    start_urls = ['https://www.ulule.com/195metres-film/']

    def parse(self, response):


        json_data = response.xpath('//script[contains(text(),"project: {")]/text()').extract_first('').strip()

        name = response.xpath('//meta[@property="og:title"]/@content').extract_first()
        short_description = response.xpath('//meta[@property="og:description"]/@content').extract_first()

        no_of_supporters = re.findall(r'"supporters_count": (\d+)', json_data)[0]


        amount=re.findall(r'"amount_raised": (\d+)', json_data)[0]
        currency=re.findall(r'"currency".*?",',json_data)[0]
        goals = re.findall(r'"goal": (\d+)', json_data)[0]
        goal={'amount':goals,'currency':currency}
        percentage_funded = float(re.findall(r'"percent": (\d+)', json_data)[0])

        fund_raised = {}
        amount = re.findall(r'"amount_raised": (\d+)', json_data)[0]
        cu = re.findall(r'"currency".*?",', json_data)[0].strip(',').strip('"')
        currency = cu.strip('currency": "')
        fund={'amount':amount,'currency':currency}
        fund_raised.update(fund)
        days_left=re.findall(r'"date_end".*?",',json_data)[0].strip(',').strip('"')
        date_end='campaign ended the',days_left.strip('"date_end": "')

        imag= re.findall(r'75x75": {"height": 20, "url":.*?",',json_data)[0]
        image=re.findall(r'url":.*?jpg', imag)[0]


        location = re.findall(r' "location": .*?",', json_data)[1].strip('"')
        url=response.url
        creator={'name':name,'url':url,' ':image,'':location}
        video=re.findall(r'"video".*?",',json_data)[1].strip('"video"')
        text = re.findall(r'"description".*?",', json_data)[0].strip('description"')

        description={'text':text}
        projectowner=re.findall(r'"description_yourself".*?,',json_data)
        teammember=re.findall(r'left;\".*?,',json_data)




        item= UlulItem(
            name = name,
            short_description = short_description,
            no_of_supporters = no_of_supporters,
            fund_raised=fund_raised,
            goal=goal,
            date_end=date_end,
            creator=creator,
            video=video,
            description=description,
            projectowner=projectowner,
            teammember=teammember,




        )
        yield item

