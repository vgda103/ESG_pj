import scrapy
import json
import csv
from naverstock_crawling.items import ESGItem

class esgSpider(scrapy.Spider):
    name = "naverstock"

    def start_requests(self):
        # CSV 파일에서 종목 코드 추출
        with open(r'C:\Users\yobab\Desktop\workspace\study\crawl\m.naverstock_esg\naverstock_crawling\naverstock_crawling\data_1405_20240407.csv', newline='', encoding='cp949') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # 헤더 행 스킵
            for row in reader:
                stock_number = row[1]  # 두 번째 열에 있는 단축코드 추출
                url = f'https://m.stock.naver.com/api/stock/{stock_number}/finance/nonFinance'
                yield scrapy.Request(url, callback=self.parse, meta={'stock_number': stock_number})

    def parse(self, response):
        stock_number = response.meta['stock_number']
        json_data = json.loads(response.text)
        
        # ESG 항목이 있는지 확인
        if 'nonFinanceInfo' in json_data:
            # E, S, G 항목 처리
            for theme in ['E', 'S', 'G']:
                theme_items = []                      #['E01'] # 용수 재활용률 ['E03'] # 에너지 사용량 ['E05'] # 미세먼지 배출량 ['E01'] # 용수 재활용률 ['E04'] # 폐기물 재활용률
                for i in range(1, 6):                 #['S05'] # 직원평균연봉  ['S04'] # 비정규직고용률 ['S01'] # 기부금 ['S02'] # 직원평균근속년수
                    indicator_code = f'{theme}0{i}'   #['G03'] # 사외이사비율  ['G05'] # 최대주주지분율 ['G04'] # 이사회의 독립성 ['G01'] # 사내등기임원 평균보수 ['G02'] # 임원/직원 보수 비율
                    if indicator_code in json_data['nonFinanceInfo'][theme]:
                        for sel in json_data['nonFinanceInfo'][theme][indicator_code]:
                            if sel.get('baseYear') == '2021':
                                theme_items.append({
                                    'theme': theme,
                                    'indicatorCode': indicator_code,
                                    'score': sel.get('score'),         #score 회사 점수  
                                    'industryAvg': sel.get('industryAvg')  #industryAvg 업종 평균
                                })
                    else:
                        self.logger.warning(f'{stock_number} 종목에 {theme} 항목이 없거나 해당 항목이 존재하지 않습니다.')
                
                # 각 항목에 대한 정보를 ESGItem으로 포장하여 반환
                for item in theme_items:
                    esg_item = ESGItem(
                        stock_number=stock_number,
                        themeCode=item['theme'],
                        indicatorCode=item['indicatorCode'],
                        score=item['score'],
                        industryAvg=item['industryAvg']
                    )
                    yield esg_item
        else:
            self.logger.warning(f'ESG 정보가 없는 종목: {stock_number}. 건너뜁니다.')


      






