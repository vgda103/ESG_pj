# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EsgReportItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    report_no = scrapy.Field()
    company_name = scrapy.Field()
    rate_year = scrapy.Field()
    pdf_file = scrapy.Field()
    txt_file = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    pass
