import requests
from bs4 import BeautifulSoup
import urllib.parse
import time
import pandas as pd
import os

# 키워드별 검색결과 
# 데이터 검색 기간과 키워드를 받아 한경뉴스를 검색하여 dictionary 타입의 결과물을 return 해주는 함수
def hankyung_crawler(sdate, edate, keyword):

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
        url = f'https://search.hankyung.com/search/news?query={keyword_encoded}&sort=DATE%2FDESC%2CRANK%2FDESC&period=DATE&area=ALL&sdate={start_date}&edate={end_date}&exact=&include=&except=&page={page}'

        res = requests.get(url, headers = {'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(res.text, 'html.parser')

        time.sleep(1)

        li_tags = soup.select('ul.article li')
        for li_tag in li_tags:
            try:
                date = li_tag.select_one('div p.info span.date_time ').text
                href = li_tag.select_one('div.txt_wrap a').attrs['href']

                re = requests.get(href, headers ={'User-Agent': 'Mozilla/5.0'} )
                soup2 = BeautifulSoup(re.text, 'html.parser') 

                time.sleep(2)

                title, article = '', ''

                try:
                    title = soup2.select_one('article h1.headline').text.strip()
                    contents = soup2.select('.article-body')
                    for content in contents:
                        article += content.text.strip().replace('\n', ' ')

                except:
                    print('Failed to retrieve article from ', href)
                    pass

                                
                if title and article:
                    if title not in datas['title']:
                        datas['title'].append(title)
                        datas['date'].append(date[:10])
                        datas['article'].append(article)
                        datas['company'].append(cnm)
                        datas['keyword'].append(keyword.split('+')[1])

            except:
                pass


        if soup.select_one('div.search_none') != None and '에 대한 검색결과가 없습니다.' in soup.select_one('div.search_none').text: 
            print(f'{keyword} 크롤링 완료')   
            end_point = True

        else:
            continue


    return datas

# 기업별 키워드 리스트 검색결과
# 기업명, 키워드리스트와 검색기간을 받아 한경뉴스를 검색하여 dictionary 타입의 결과물을 return 해주는 함수
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

        cnm_kw_datas = hankyung_crawler(start_date, end_date, keyword=keyword)
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
cnm_list

# 검색기간 지정
start_date = '2023.01.01'
end_date = '2023.12.31'

for cnm in cnm_list:
    if not os.path.exists(f'./한경뉴스_{cnm}.csv'):
        cnm_kw_df = pd.DataFrame(cnm_kw_crawler(cnm, kword_list, start_date, end_date))
        cnm_kw_df['category'] = [kwords_df[kwords_df['키워드']==keyword]['카테고리'].values[0] for keyword in cnm_kw_df['keyword']]
        cnm_kw_df.to_csv(f'./한경뉴스_{cnm}.csv', index=False)