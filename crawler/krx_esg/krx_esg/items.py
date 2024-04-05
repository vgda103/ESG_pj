# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class KrxEsgItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    COM_ABBRV = scrapy.Field()
    KCGS_ESG = scrapy.Field()
    KCGS_ENV = scrapy.Field()
    KCGS_SOC = scrapy.Field()
    KCGS_GOV = scrapy.Field()
    RPT_YN = scrapy.Field()
    pass

   
    
