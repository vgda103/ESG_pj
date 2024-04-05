#!/usr/bin/env python3

import scrapy

class MySpider(scrapy.Spider):
    name = 'krs_report'

    start_num = 1
    end_num = 15   
    
    url = 'https://ksaesg.or.kr/p_base.php?action=h_report_04&board_id=&s_text=&s_category='

    start_urls = []
    for i in range(1, end_num +1):
        start_urls.append(f'{url}&page={i}') 

    def parse(self, response): 

        base_url = 'https://ksaesg.or.kr/p_base.php'
        # pdf_url = 'pop_file_download.php?target=display&img_type=img_list'

        param = 'action=h_report_04_detail&page=1&s_text=&s_category=&1=1'

        tag = response.css('.table > tbody > tr')

        for sel in tag:           
            # title = sel.css('td > a::text').get()
            detail_url = sel.css('td > a::attr(href)').get()

            # report no 추출을 위한 분리 처리
            spl_list = detail_url.split('no=')
            report_list = spl_list[1].split('&')
            report_no = report_list[0] # report no

            # url = response.url
            comp_name = sel.css('tr > th::text').get() # 회사명
            rate_year = sel.css('tr > td::text').get() # 평가년도
            rate_year = rate_year.replace('년', '')
            report_name = sel.css('td > a::text').get() # 리포트명

            next_link = f'{base_url}?{param}&no={report_no}'

            # print(next_link)

            yield scrapy.Request(
                next_link, 
                callback=self.parse_det, 
                meta={
                    # 'url': url, 
                    # 'path': path
                    'report_no': report_no,
                    'comp_name': comp_name,
                    'rate_year': rate_year,
                    'report_name': report_name,
                }
            )

    def parse_det(self, response):
        def extract_with_css(query):
            return 'https://ksaesg.or.kr/' + response.css(query).get(default='').strip()
        
        print('*'*100)
        print(response.meta['report_no'], ' 진행 중..')

        yield {
            # 'path':response.meta['path'],
            'file_urls': [extract_with_css('.table > tbody > tr > td > a::attr(href)')],
            # 'url':response.meta['url']
            'report_no': response.meta['report_no'], 
            'comp_name': response.meta['comp_name'],
            'rate_year': response.meta['rate_year'],
            'report_name': response.meta['report_name'],
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
    'FEED_EXPORT_ENCODING': 'utf-8'
})

c.crawl(MySpider)
c.start()