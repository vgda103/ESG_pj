# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ESGItem(scrapy.Item):
    # 종목 번호
    stock_number = scrapy.Field()
    # 항목 테마 코드 (E, S, G)
    themeCode = scrapy.Field()
    # 지표 코드
    indicatorCode = scrapy.Field()
    # 점수
    score = scrapy.Field()
    # 산업 평균
    industryAvg = scrapy.Field()
    # 기타 필요한 필드들을 여기에 추가할 수 있습니다.
    # 예를 들어, indicatorName, indicatorUnit 등


    pass