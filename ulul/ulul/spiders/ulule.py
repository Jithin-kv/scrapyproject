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
        image=re.findall(r'https:.*?jpg', imag)[0]


        loc = re.findall(r' "location": .*?",', json_data)[1].strip('"')
        location = loc.strip('location": "').strip('",')
        url=response.url
        creator={'name':name,'url':url,'image':image,'location':location}
        video=re.findall(r'"video".*?",',json_data)[1].strip('"video"')
        tex = re.findall(r'"description".*?",', json_data)[0].strip('description"')
        text = re.findall(r'Thanks.*?",', tex)[0].strip('\\').strip('//').strip()
        dimag=re.findall(r' "url".*?",',json_data)

        description={'images':dimag,'text':text}
        project=re.findall(r'"description_yourself".*',json_data)[0]
        projectownername1 = re.findall(r'Ale.*?mo', json_data)[0]
        projectownername2 = re.findall(r'Marco Fortunati', json_data)[0]
        projectownername3 = re.findall(r'Maria Tsaousi', json_data)[0]

        projectownerdes1=re.findall(r'A cine.*?of the film',json_data)[0]
        projectownerdes2 = re.findall(r'Cinematography.*?editor of the film', json_data)[0]
        projectownerdes3 = re.findall(r'I am a Cypriot.*?Cyprus.', json_data)[0]
        projectownerimage = re.findall(r'"https://d2homsd77vx6d2.*?jpg', project)
        projectownerimage1 = re.findall(r'src.*?jpg', project)[0].strip('src=\\"')
        projectownerimage2=projectownerimage[1]
        projectownerimage3=projectownerimage[2]
        projectowner=[{'name':projectownername1,'desc':projectownerdes1,'image':projectownerimage1},{'name':projectownername2,'desc':projectownerdes2,'image':projectownerimage2}
                      ,{'name':projectownername3,'desc':projectownerdes3,'image':projectownerimage3}]

        teammember1 = re.findall(r'Marian.*?cci', project)[0]
        teammemberdes1 = re.findall(r'I am an assistant director.*?assistant', project)[0]
        teammemberimage1 = projectownerimage[3]

        teammember2 = re.findall(r'Guappecart', project)[0]
        teammemberdes2 = re.findall(r'We are an.*?of the film.', project)[0]
        teammemberimage2 = projectownerimage[4]
        teammember3 = re.findall(r'Maria Efthymiou', project)[0]
        teammemberdes3 = re.findall(r'I am a f.*?."', project)[0]
        teammemberimage3 = projectownerimage[5]
        teammember = [{'name': teammember1, 'desc': teammemberdes1, 'image': teammemberimage1},{'name':teammember2,'desc':teammemberdes2,'image':teammemberimage2},
                      {'name':teammember3,'desc':teammemberdes3,'image':teammemberimage3}]



        item= UlulItem(
            name = name,
            short_description = short_description,
            no_of_supporters = no_of_supporters,
            percentage_funded=percentage_funded,
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

