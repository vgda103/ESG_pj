import os 
import re
import pandas as pd
import sys

download_path = r'' # file_path 지정

cleansed_news = {
    'company':[],
    'category':[],
    'keyword':[],
    'title':[],
    'date':[],
    'article':[]
}

def hankyung_cleanser(df):
    for idx, row in df.iterrows():
        article = row['article']
        if row['title'] not in cleansed_news['title'] and row['company'] in article and row['keyword'] in article: # 중복기사 및 무관한 기사 필터링
            if len([p for p in re.finditer(r'[0-9]',article )]) < len([p for p in re.finditer(r'[가-힇a-zA-Z]', article)]): # 실적 현황 등의 발간물 필터링
                if '본 글은 투자 참고용입니다.' not in article: # 투자종목 추천 필터링
                    email_pattern = r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)' # email 제거
                    article = re.sub(email_pattern, '', string=article)
                    url_pattern = r'(http|ftp|https)://(?:[-\w.]|(?:%[\da-fA-F]{2}))+' # url 제거
                    article = re.sub(url_pattern, '', string=article)
                    pattern = r'[※].*?(\.)'
                    article = re.sub(pattern, '', string=article)
                    pattern = r'<[가-힇].*?>'
                    article = re.sub(pattern, '', string=article)
                    pattern = r'[가-힇]...기자'
                    article = re.sub(pattern, '', string=article)
                    article = re.sub(r'[-=+#/\?:^$@*\"※~&%ㆍ!』\\\'|\(\)\[\]\<\>`\'…》]','', string=article)
                    pattern = r'[^(가-힇A-Za-z., \t)]'
                    article = re.sub(pattern, '', string = article)
                    article = article.strip()
                    cleansed_news['company'].append(row['company'])
                    cleansed_news['category'].append(row['category'])
                    cleansed_news['keyword'].append(row['keyword'])
                    cleansed_news['title'].append(row['title'])
                    cleansed_news['date'].append(row['date'])
                    cleansed_news['article'].append(article)
    
    return pd.DataFrame(cleansed_news)

for news in os.listdir(download_path):
    df = pd.read_csv(download_path+news)
    hankyung_cleanser(df).to_csv('./cleansed_hankyung.csv', index=False)