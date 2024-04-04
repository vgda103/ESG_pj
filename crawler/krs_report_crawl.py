#!/usr/bin/env python3

import scrapy

class MySpider(scrapy.Spider):
    name = 'myspider'

    start_num = 1
    end_num = 15    
    url = 'https://ksaesg.or.kr/p_base.php?action=h_report_04&board_id=&s_text=&s_category='

    start_urls = []

    for i in range(1, end_num +1):
        start_urls.append(f'{url}&page={i}') 

    def parse(self, response):

        # for link in response.css('.default .er').xpath('@href').extract():
        #      url = response.url
        #      path = response.css('ol.breadcrumb li a::text').extract()
        #      next_link = response.urljoin(link)

        #      yield scrapy.Request(next_link, callback=self.parse_det, meta={'url': url, 'path': path})

        base_url = 'https://ksaesg.or.kr/p_base.php'
        # pdf_url = 'pop_file_download.php?target=display&img_type=img_list'

        param = 'action=h_report_04_detail&page=1&s_text=&s_category=&1=1'

        tag = response.css('.table > tbody > tr')

        for sel in tag:           
            # title = sel.css('td > a::text').get()
            detail_url = sel.css('td > a::attr(href)').get()

            spl_list = detail_url.split('no=')
            no_list = spl_list[1].split('&')

            # print(detail_url)           

            url = response.url
            path = sel.css('td > a::text').get()
            next_link = f'{base_url}?{param}&no={no_list[0]}'

            # print(next_link)

            yield scrapy.Request(next_link, callback=self.parse_det, meta={'url': url, 'path': path})


    def parse_det(self, response):
        # print(response.url)
        # print(response.css('.table > tbody > tr > td > a::attr(href)').get(default='').strip())

        domain_url = 'https://ksaesg.or.kr'
        file_url = domain_url + '/' + response.css('.table > tbody > tr > td > a::attr(href)').get()

        # print(file_url)

        def extract_with_css(query):
            return 'https://ksaesg.or.kr/' + response.css(query).get(default='').strip()

        yield {
            'path':response.meta['path'],
            # 'file_urls': [extract_with_css('a.btn.btn-primary::attr(href)')],
            'file_urls': [extract_with_css('.table > tbody > tr > td > a::attr(href)')],
            'url':response.meta['url']
        }


from scrapy.crawler import CrawlerProcess

c = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0',

    # save in file as CSV, JSON or XML
    'FEED_FORMAT': 'csv',     # csv, json, xml
    'FEED_URI': 'output.csv', # 

    # download files to `FILES_STORE/full`
    # it needs `yield {'file_urls': [url]}` in `parse()`
    'ITEM_PIPELINES': {'scrapy.pipelines.files.FilesPipeline': 1},
    'FILES_STORE': '.',
    'LOG_LEVEL': 'ERROR',
})
c.crawl(MySpider)
c.start()