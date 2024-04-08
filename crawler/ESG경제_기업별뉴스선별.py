import pandas as pd
import sys
import re

testset_df = pd.read_csv('./output.csv', encoding= 'utf-8')
cnm_list = list(testset_df['COM_ABBRV'])

env_so_df = pd.read_csv('./ESG경제_환경_사회.csv')
co_gov_df = pd.read_csv('./ESG경제_기업_거버넌스.csv')

ESG_news_df = pd.merge(env_so_df,co_gov_df, how="outer")

cnm_articles = {
    'company':[],
    'category':[],
    'title':[],
    'date': [],
    'article':[]
}

for cnm in cnm_list:
    for article in list(ESG_news_df['article']):
        if cnm in article:
            cnm_articles['company'].append(cnm)
            cnm_articles['category'].append(ESG_news_df[ESG_news_df['article'] == article]['category'].values[0])
            cnm_articles['title'].append(ESG_news_df[ESG_news_df['article'] == article]['title'].values[0])
            cnm_articles['date'].append(ESG_news_df[ESG_news_df['article'] == article]['date'].values[0])

            sys.path.append(r'./') 
            from common import comm

            tab_pattern = r'\[.*?\]' 
            article = re.sub(tab_pattern, "", string=article) 

            article = comm.clean_text(article) 

            cnm_articles['article'].append(article)


(pd.DataFrame(cnm_articles)).to_csv('./ESG경제_기업별뉴스.csv', index=False)