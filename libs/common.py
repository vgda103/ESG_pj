# -*- config: utf-8 -*-
# 공통 함수 모음

import os
import re
import pandas as pd

class comm:
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
    
    def missing_data(path=str, file=str, encode=str):
        file_path = path + file

        if os.path.isfile(file_path):
            origin_data = pd.read_csv(file_path, encoding=encode)
            df = origin_data.copy()
            # print(df)
        else:
            return print('존재하지 않는 파일입니다.')
        
        # df.head()

        # 리스트 총 개수
        print('리스트 총 개수: ', df.shape, '\n')

        # 결측치 확인
        print('결측치 확인: ', df.isnull().sum(), '\n')
        
        return df