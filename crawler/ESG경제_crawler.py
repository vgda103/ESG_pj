import pandas as pd
import requests
from bs4 import BeautifulSoup

code_list = {'환경_사회':'S1N2', '기업_거버넌스':'S1N8' }

for code_category, code in code_list.items():
    total_page = 1000
    page = 1

    datas = {
        'category':[],
        'title':[],
        'date': [],
        'article':[]
    }

    while page < total_page:

        num = page

        url = f'https://www.esgeconomy.com/news/articleList.html?page={page}&total={total_page}&box_idxno=&sc_section_code={code}&view_type=sm'
        res = requests.get(url)

        soup = BeautifulSoup(res.text, 'html.parser')
        li_tags = soup.select('section ul li')

        for li_tag in li_tags:
            try:
                title = li_tag.select_one('div h4').text
                news_href = li_tag.select_one('div p a').attrs['href']

                re = requests.get('https://www.esgeconomy.com/'+news_href)
                soup2 = BeautifulSoup(re.text, 'html.parser')

                article = ''
                contents = soup2.select('article p') #<p>...</p> tag 가 붙은 뉴스 본문
                for content in contents:
                    article += content.text

                category = li_tag.select('div span em')[0].text
                date = li_tag.select('div span em')[2].text

            except: pass

            if int(date[:4]) >= 2023:

                if title not in set(datas['title']):
                
                    datas['category'].append(category)
                    datas['title'].append(title)
                    datas['date'].append(date[:11])
                    datas['article'].append(article)

            else:
                break
       
        page += 1

        if num == page:
            break

    pd.DataFrame(datas).to_csv(f'./ESG경제_{code_category}.csv', index=False)
    print(f'{code_category} 크롤링 완료')

    if code_category == '기업_거버넌스':
        print('ESG경제 크롤링이 완료되었습니다. 프로그램이 종료됩니다.')