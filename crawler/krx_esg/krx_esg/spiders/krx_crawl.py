# import scrapy
# import json
# from krx_esg.items import KrxEsgItem

# class krxSpider(scrapy.Spider):
#     name = "krx"

#     def start_requests(self):
#         target_url = 'https://esg.krx.co.kr/contents/99/ESG99000001.jspx'
#         param = 'sch_com_nm=&sch_yy=2024&pagePath=%2Fcontents%2F02%2F02020000%2FESG02020000.jsp&code=02%2F02020000%2Fesg02020000'
        
#         yield scrapy.Request(                    
#             url=f'{target_url}?{param}&{curPage=1}',
#             callback=self.parse_news
#         )       

#     def parse_news(self, response):
#         item = KrxEsgItem()
#         data = json.loads(response.text)
#         news_cnt = len(data['result'])
        
#         for i in range(0, news_cnt):
#             # com_abbrv = data['result'][i]['com_abbrv'] # 회사명
#             # kcgs_esg = data['result'][i]['kcgs_esg'] # 종합등급
#             # kcgs_env = data['result'][i]['kcgs_env'] # 환경
#             # kcgs_soc = data['result'][i]['kcgs_soc'] # 사회
#             # kcgs_gov = data['result'][i]['kcgs_gov'] # 지배구조
#             # rpt_yn = data['result'][i]['rpt_yn'] # 지속가능경영보고서공시여부 
            
#             item['COM_ABBRV'] = data['result'][i]['com_abbrv']
#             item['KCGS_ESG'] = data['result'][i]['kcgs_esg']
#             item['KCGS_ENV'] = data['result'][i]['kcgs_env']
#             item['KCGS_SOC'] = data['result'][i]['kcgs_soc']
#             item['KCGS_GOV'] = data['result'][i]['kcgs_gov']
#             item['RPT_YN'] = data['result'][i]['rpt_yn']  
            
#             print(item['COM_ABBRV'], item['KCGS_ESG'], item['KCGS_ENV'], item['KCGS_SOC'], item['KCGS_GOV'], item['RPT_YN'])
            #print(item['COM_ABBRV'])

        # count = 0
        # batchcount = 100
        # for sel in data['result']:
            # print(sel)
            # for key, value in sel.items():
                #value = ['com_abbrv', 'kcgs_yy', 'kcgs_esg', 'kcgs_env', 'kcgs_soc', 'kcgs_gov', 'msci_esg']                
                # print(f"key: {key}' - 'value: {value ='com_abbrv', 'kcgs_yy', 'kcgs_esg', 'kcgs_env', 'kcgs_soc', 'kcgs_gov', 'msci_esg'")
                # my_dict = {'name': 'John', 'age': 30, 'city': 'New York'}

# 딕셔너리의 키를 순회하면서 각 키와 해당하는 값을 출력
    # for key in my_dict'com_abbrv' 'kcgs_esg' 'kcgs_env'  'kcgs_soc'  'kcgs_gov'  'msci_esg'
    #     value = my_dict[key]
    #     print(f'{key}: {value}')

            
        # count += 1
        # if count >= batchcount:
        #     return
        # print(data['result'][0]['kcgs_soc'])    

            # time.sleep(0.5)
            # yield item
import scrapy
import json
from krx_esg.items import KrxEsgItem

class krxSpider(scrapy.Spider):
    name = "krx"
    start_page = 1
    total_pages = 80

    def start_requests(self):
        target_url = 'https://esg.krx.co.kr/contents/99/ESG99000001.jspx'
        param = 'sch_com_nm=&sch_yy=2024&pagePath=%2Fcontents%2F02%2F02020000%2FESG02020000.jsp&code=02%2F02020000%2Fesg02020000'        
        
        for page_num in range(self.start_page, self.total_pages + 1):
            yield scrapy.Request(                    
                url=f'{target_url}?{param}&curPage={page_num}',
                callback=self.parse_news
            )

    def parse_news(self, response):
        item = KrxEsgItem()
        data = json.loads(response.text)
        news_cnt = len(data['result'])        
        
        # print(news_cnt)
        for i in range(0, news_cnt):
            item['COM_ABBRV'] = data['result'][i]['com_abbrv'] # 회사명
            item['KCGS_ESG'] = data['result'][i]['kcgs_esg'] # 종합등급
            item['KCGS_ENV'] = data['result'][i]['kcgs_env'] # 환경
            item['KCGS_SOC'] = data['result'][i]['kcgs_soc'] # 사회
            item['KCGS_GOV'] = data['result'][i]['kcgs_gov'] # 지배구조
            item['RPT_YN'] = data['result'][i]['rpt_yn']     # 지속가능경영보고서공시여부      
            
            # print(item['COM_ABBRV'], item['KCGS_ESG'], item['KCGS_ENV'], item['KCGS_SOC'], item['KCGS_GOV'], item['RPT_YN'])
        
            yield item