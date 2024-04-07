# 텍스트 정제 및 저장

import os
import fitz
import re

# 텍스트 정제 함수
def clean_text(text):
    email_pattern = r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)' # email 제거
    text = re.sub(email_pattern, '', string=text)

    url_pattern = r'(http|ftp|https)://(?:[-\w.]|(?:%[\da-fA-F]{2}))+' # url 제거
    text = re.sub(url_pattern, '', string=text)

    no_meaning_pattern = r'([ㄱ-ㅎㅏ-ㅣ]+)'  # 한글 자음, 모음
    text = re.sub(no_meaning_pattern, '', string=text)

    num_pattern = r'(\d)+' # 숫자 제거
    text = re.sub(num_pattern, '', string=text) 

    symbol_pattern = '[-=+,#/\:^*\"※~&ㆍ』\\‘|\(\)\[\]\<\>`\'…》▲▼■•●%]'
    text = re.sub(symbol_pattern,'', string=text) # 특수문자 제거

    # tab_pattern = r"^\s+|\s+$" # 양쪽 공백 제거
           
    tab_pattern = r'\t' # 탭 제거
    text = re.sub(tab_pattern, "", string=text) 

    pattern = r'^.*?기자]'
    text = re.sub(pattern, '' , string=text)

    pattern = r'^.*?특파원]'
    text = re.sub(pattern, '' , string=text)

    return text

path = '../../files/ksa_report/'
pdf_list = os.listdir(path+'pdf')

for pdf in pdf_list:
    file_no = re.sub(r'[^0-9]', '', pdf)
    doc = fitz.open(path+'/pdf/'+pdf)
    file_path = path+'txt/'+file_no+'.txt'

    text = ''
    for page in doc:
        text += page.get_text().replace('\n', '')

    print('*'*100)
    print(f'{file_no}.txt 진행 중..')

    contents = clean_text(text) # 텍스트 정제

    with open(file_path, 'w', encoding='utf-8') as f: # 텍스트 파일 저장
        f.write(contents)