import pandas as pd
import requests
from bs4 import BeautifulSoup

award_list = ['h_ksi', 'h_krca']

awarded_list = []
for award in award_list:
    url = f'https://ksaesg.or.kr/p_base.php?action={award}'
    res = requests.get(url)

    soup = BeautifulSoup(res.text, 'html.parser')

    awarded_cnms = soup.select('.table-search table tbody tr th')
    for cnm in awarded_cnms:
        awarded_list.append(cnm.text)
    
df = pd.DataFrame(awarded_list, columns=['수상업체명'])
df.to_csv('./KSA_수상기업목록.csv', index=False)
