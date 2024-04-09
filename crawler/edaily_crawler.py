import requests
from bs4 import BeautifulSoup
import urllib.parse
import time
import pandas as pd

# 키워드별 검색결과
# 데이터 검색 기간과 키워드를 받아 이데일리 뉴스를 검색하여 dictionary 타입의 결과물을 return 해주는 함수
def edaily_crawler(sdate, edate, keyword):
    # sdate, edate = 'YYYY.MM.DD' 형식의 str
    # keyword = f'{기업}+{키워드}' 형식의 str 검색어

    end_point = False
    page = 0
    datas = {
        'company':[],
        'keyword':[],
        'title':[],
        'date': [],
        'article':[]
    }
    print(f'{keyword}에 대한 크롤링을 시작합니다.')
    while end_point == False:
        page +=1
        keyword_encoded = urllib.parse.quote_plus(keyword)
        url = f'https://www.edaily.co.kr/search/news/?source=ticon&keyword={keyword_encoded}&include=&exclude=&jname=&start={start_date}&end={end_date}&sort=latest&date=pick&exact=false&page={page}'

        res = requests.get(url, headers = {'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(res.text, 'html.parser')
        time.sleep(1)
        div_tags = soup.select('div#newsList div.newsbox_04')
        if div_tags != []:
            for div_tag in div_tags:
            
                try:
                    title = div_tag.select_one('a').attrs['title']
                    date = div_tag.select_one('div.author_category').text.strip()
                    href1 = div_tag.select_one('a').attrs['href']
                    href = 'https://www.edaily.co.kr/' + href1

                    re = requests.get(href, headers ={'User-Agent': 'Mozilla/5.0'} )
                    soup2 = BeautifulSoup(re.text, 'html.parser')
                    time.sleep(2)
                    article = ''
                    try:
                        contents = soup2.select('div.news_body')
                        for content in contents:
                            article += content.text.strip()
                    except:
                        print('Failed to retrieve article from ', href)
                        pass
                except:
                    pass
                
                if title not in datas['title'] and article != '':
                    datas['title'].append(title)
                    datas['date'].append(date[:10])
                    datas['article'].append(article)
                    datas['company'].append(cnm)
                    datas['keyword'].append(keyword.split('+')[1])

        else:
            end_point = True

    return datas

# 기업별 키워드 리스트 검색결과
# 기업명, 키워드리스트와 검색기간을 받아 이데일리 뉴스를 검색하여 dictionary 타입의 결과물을 return 해주는 함수
def cnm_kw_crawler(cnm, keyword_list, start_date, end_date):
    # cnm = 기업명 (str)
    # keyword_list = 키워드 리스트 (list)
    # sdate, edate = 'YYYY.MM.DD' 형식의 str
    cnm_datas = {
            'company':[],
            'keyword':[],
            'title':[],
            'date': [],
            'article':[]
        }
    for kword in keyword_list:
        keyword = f'{cnm}+{kword}'
        end_point = False
        page = 0
        datas = {
            'company':[],
            'keyword':[],
            'title':[],
            'date': [],
            'article':[]
        }
        cnm_kw_datas = edaily_crawler(start_date, end_date, keyword=keyword)
        cnm_datas['title'].extend(cnm_kw_datas['title'])
        cnm_datas['date'].extend(cnm_kw_datas['date'])
        cnm_datas['article'].extend(cnm_kw_datas['article'])
        cnm_datas['company'].extend(cnm_kw_datas['company'])
        cnm_datas['keyword'].extend(cnm_kw_datas['keyword'])
    return cnm_datas

# 키워드 리스트 가져오기
kwords_df = pd.read_csv('./크롤링_키워드리스트.csv')
kword_list = list(kwords_df['키워드'])
# 기업 리스트 가져오기
testset_df = pd.read_csv('./output.csv', encoding= 'utf-8')
cnm_list = list(testset_df['COM_ABBRV'])

# 검색기간 지정
start_date = '20230101'
end_date = '20231231'

for cnm in cnm_list:
    cnm_kw_df = pd.DataFrame(cnm_kw_crawler(cnm, kword_list, start_date, end_date))
    cnm_kw_df['category'] = [kwords_df[kwords_df['키워드']==keyword]['카테고리'].values[0] for keyword in cnm_kw_df['keyword']]
    cnm_kw_df.to_csv(f'./이데일리뉴스_{cnm}.csv', index=False)