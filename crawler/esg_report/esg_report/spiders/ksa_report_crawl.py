### Python 3 ###
# -*- config: utf-8 -*-

import scrapy
from esg_report.items import EsgReportItem
import traceback
import pandas as pd
import os

class KsaSpider(scrapy.Spider):    
    name = 'ksa'
    allowed_domains = ['ksaesg.or.kr']
    start_num = 1
    end_num = 15
    
    url = 'https://ksaesg.or.kr/p_base.php?action=h_report_04&board_id=&s_text=&s_category='

    start_urls = []
    for i in range(1, end_num +1):
        start_urls.append(f'{url}&page={i}')
        # break

    def parse(self, response): 
        base_url = 'https://ksaesg.or.kr/p_base.php'
        param = 'action=h_report_04_detail&page=1&s_text=&s_category=&1=1'

        try:
            path = '../files/krs_report/csv/'
            file_name = 'krs_crawl_20240406.csv'
            file_path = path + file_name

            # 크롤링 파일 존재 여부 확인
            if os.path.isfile(file_path):
                data_list = pd.read_csv(file_path, encoding='utf-8')
                file_yn = 1
            else:
                file_yn = 0
        
            tag = response.css('.table > tbody > tr')
            for sel in tag:
                title = sel.css('td > a::text').get()
                detail_url = sel.css('td > a::attr(href)').get()

                # report no 추출을 위한 분리 처리
                spl_list = detail_url.split('no=')
                report_list = spl_list[1].split('&')
                report_no = report_list[0] # report no

                if file_yn == 1:
                    dupl = 0 # 중복 여부(0: 중복안됨, 1: 중복)
                    
                    # 중복 체크(report_no)                
                    for i in data_list.loc[:, 'report_no']:
                        if str(i) == report_no:
                            dupl = 1
                            break
                    if dupl == 1:
                        continue

                # url = response.url
                company_name = sel.css('tr > th::text').get() # 회사명

                rate_year = sel.css('tr > td::text').get() # 평가 년도
                rate_year = rate_year.replace('년', '')
                                
                pdf_file = report_no + '.pdf' # pdf 파일명
                txt_file = report_no + '.txt' # txt 파일명
                next_link = f'{base_url}?{param}&no={report_no}'

                yield scrapy.Request(
                    next_link, 
                    callback=self.parse_det, 
                    meta={                       
                        'title': title,
                        'report_no': report_no,
                        'company_name': company_name,
                        'rate_year': rate_year,
                        'pdf_file': pdf_file,
                        'txt_file': txt_file,
                    }
                )
        except Exception as e:
            trace_back = traceback.format_exc()
            message = str(e) + '\n' + str(trace_back)
            print(message)            
    
    def parse_det(self, response):
        item = EsgReportItem()
        try:
            def extract_with_css(query):
                return ['https://ksaesg.or.kr/' + response.css(query).get(default='').strip()]
            
            item['title'] = response.meta['title']
            item['report_no'] = response.meta['report_no']
            item['company_name'] = response.meta['company_name']
            item['rate_year'] = response.meta['rate_year']
            item['pdf_file'] = response.meta['pdf_file']
            item['txt_file'] = response.meta['txt_file']
            item['file_urls'] = extract_with_css('.table > tbody > tr > td > a::attr(href)')            

            print('*'*100)
            print(response.meta['report_no'], ' 진행 중..')        

            yield item
        except Exception as e:
            trace_back = traceback.format_exc()
            message = str(e) + '\n' + str(trace_back)
            print(message)            