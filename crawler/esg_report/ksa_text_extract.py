# -*- config: utf-8 -*-
# 텍스트 정제 및 저장

import os
import fitz
import re
import sys
sys.path.append("../../.")
from libs.common import comm

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

    contents = comm.clean_text(text) # 텍스트 정제

    with open(file_path, 'w', encoding='utf-8') as f: # 텍스트 파일 저장
        f.write(contents)