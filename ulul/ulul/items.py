# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UlulItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    short_description=scrapy.Field()
    no_of_supporters= scrapy.Field()
    fund_raised=scrapy.Field()
    date_end=scrapy.Field()
    creator=scrapy.Field()
    video=scrapy.Field()
    description=scrapy.Field()
    projectowner=scrapy.Field()
