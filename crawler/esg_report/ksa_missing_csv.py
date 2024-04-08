# 결측치 처리
import os
import pandas as pd

import sys
sys.path.append("../../.")
from libs.common import comm

# path = '../../../files/ksa_report/csv/'
path = '../../files/ksa_report/csv/'
file_name = 'ksa_crawl_20240407.csv'

comm.missing_data(path, file_name, 'cp949')

# 결측치 확인 후 해당 컬럼 및 행 삭제
df = df.drop(labels='files', axis=1) # axis: {0 : index / 1 : columns} 
df = df.drop(labels='file_urls', axis=1)

print(df.columns)

# 다운로드 여부 열 생성
if 'download_yn' in df.columns:
    pass
else:
    df['download_yn'] = 0 # 디폴트 값(0: 실패)

# 다운로드 파일 확인
pdf_list = df['pdf_file'] 

for pdf in pdf_list:
    if os.path.isfile('../../files/ksa_report/pdf/'+pdf):
        df.loc[df['pdf_file'] == pdf, 'download_yn'] = 1 # 다운로드 성공: 1 로 변경(실패: 0)

pdf_list = df[df['download_yn'] == 1].reset_index(drop=False)

# 다운로드한 리스트 개수
print('다운로드 개수: ', pdf_list.shape)

pdf_non = df[df['download_yn'] == 0].reset_index(drop=False)

print('다운로드 실패: ', pdf_non.shape)

# 다운로드 실패 행 삭제
idx = df[df['download_yn'] == 0].index
df.drop(idx, inplace=True)

print('결측지 처리 리스트', df.shape)

# DB 입력용 csv 생성
df.to_csv('output.csv', header=True, index=False, encoding='cp949')