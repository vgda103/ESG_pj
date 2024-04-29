import torch
from torch import nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import gluonnlp as nlp
# error시 /usr/local/lib/python3.10/dist-packages/mxnet/numpy/utils.py in <module>의
# bool = onp.bool 을 bool = bool 로 변경하고 save (ALT+S)하고 다시 수행
import numpy as np
from tqdm import tqdm, tqdm_notebook

# ★ Hugging Face를 통한 모델 및 토크나이저 Import
from kobert_tokenizer import KoBERTTokenizer
from transformers import BertModel

from transformers import AdamW
from transformers.optimization import get_cosine_schedule_with_warmup

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = KoBERTTokenizer.from_pretrained('skt/kobert-base-v1')
bertmodel = BertModel.from_pretrained('skt/kobert-base-v1', return_dict=False)
vocab = nlp.vocab.BERTVocab.from_sentencepiece(tokenizer.vocab_file, padding_token='[PAD]')

import pandas as pd

# 감성사전을 딕셔너리로 불러와서 문장을 [[문장, 라벨],] 형태로 만들기
file_path = '/content/drive/MyDrive/Ai/ESG_project/study/finance_data.csv'  # 파일의 경로를 적절히 수정하세요.
pd = pd.read_csv(file_path)
label_list = []
for index, row in pd.iterrows():
    if row[0] == 'negative':
      row[0] = 0
    elif row[0] == 'neutral':
      row[0] = 1
    elif row[0] == 'positive':
      row[0] = 2
    label_list.append([row[2], row[0]])
    # if index == 50:
    #   break

#train & test 데이터로 나누기
from sklearn.model_selection import train_test_split

dataset_train, dataset_test = train_test_split(label_list, test_size=0.25, random_state=0)
print(len(dataset_train))
print(len(dataset_test))

# 문장 토큰화, 패딩 클래스 (BERT 기반 모델에 대한 데이터 준비 과정을 캡슐화하여 PyTorch 파이프라인에 데이터셋을 쉽게 통합할 수 있도록 )
class BERTDataset(Dataset):
    def __init__(self, dataset, sent_idx, label_idx, bert_tokenizer, max_len,
                 pad, pair):
        transform = nlp.data.BERTSentenceTransform(
            bert_tokenizer, max_seq_length=max_len, vocab=vocab, pad=pad, pair=pair)

        self.sentences = [transform([i[sent_idx]]) for i in dataset]
        self.labels = [np.int32(i[label_idx]) for i in dataset]

    def __getitem__(self, i):
        return (self.sentences[i] + (self.labels[i], ))

    def __len__(self):
        return (len(self.labels))
    
# 문장 토큰화, 패딩 클래스

# Setting parameters
max_len = 64
batch_size = 64
warmup_ratio = 0.1
num_epochs = 5
max_grad_norm = 1
log_interval = 200
learning_rate =  5e-5

# 이제 버트토크나이저와 위에서 정의한 클래스를 적용해 토큰화와 패딩을 해준다.
tok = tokenizer.tokenize

data_train = BERTDataset(dataset_train, 0, 1, tok, max_len, True, False)
data_test = BERTDataset(dataset_test, 0, 1, tok, max_len, True, False)

# torch 형식의 dataset을 만들어 입력 데이터셋의 전처리 마무리
train_dataloader = torch.utils.data.DataLoader(data_train, batch_size = batch_size, num_workers = 2)
test_dataloader = torch.utils.data.DataLoader(data_test, batch_size = batch_size, num_workers = 2)

# Kobert 모델 구현
class BERTClassifier(nn.Module):
    def __init__(self,
                 bert,
                 hidden_size = 768,
                 num_classes = 3,   # 감정 클래스 수로 조정
                 dr_rate = None,
                 params = None):
        super(BERTClassifier, self).__init__()
        self.bert = bert
        self.dr_rate = dr_rate

        self.classifier = nn.Linear(hidden_size , num_classes)
        if dr_rate:
            self.dropout = nn.Dropout(p = dr_rate)

    def gen_attention_mask(self, token_ids, valid_length):
        attention_mask = torch.zeros_like(token_ids)
        for i, v in enumerate(valid_length):
            attention_mask[i][:v] = 1
        return attention_mask.float()

    def forward(self, token_ids, valid_length, segment_ids):
        attention_mask = self.gen_attention_mask(token_ids, valid_length)

        _, pooler = self.bert(input_ids = token_ids, token_type_ids = segment_ids.long(), attention_mask = attention_mask.float().to(token_ids.device),return_dict = False)
        if self.dr_rate:
            out = self.dropout(pooler)
        return self.classifier(out)
    
    # optimizer 최신 사용 설정
from torch.optim import AdamW

# optimizer와 schedule 설정

# BERT  모델 불러오기
model = BERTClassifier(bertmodel,  dr_rate = 0.5).to(device)

optimizer = AdamW(model.parameters(), lr=learning_rate)

# optimizer와 schedule 설정 (linear warmup and decay)
no_decay = ['bias', 'LayerNorm.weight']
optimizer_grouped_parameters = [
    {'params': [p for n, p in model.named_parameters() if not any(nd in n for nd in no_decay)], 'weight_decay': 0.01},
    {'params': [p for n, p in model.named_parameters() if any(nd in n for nd in no_decay)], 'weight_decay': 0.0}
]


optimizer = AdamW(optimizer_grouped_parameters, lr = learning_rate)
loss_fn = nn.CrossEntropyLoss() # 다중분류를 위한 loss function

t_total = len(train_dataloader) * num_epochs
warmup_step = int(t_total * warmup_ratio)

scheduler = get_cosine_schedule_with_warmup(optimizer, num_warmup_steps = warmup_step, num_training_steps = t_total)

# calc_accuracy : 정확도 측정을 위한 함수
def calc_accuracy(X,Y):
    max_vals, max_indices = torch.max(X, 1)
    train_acc = (max_indices == Y).sum().data.cpu().numpy()/max_indices.size()[0]
    return train_acc

train_dataloader

# 훈련 결과 검증 함수

def predict(predict_sentence): # input = 감정분류하고자 하는 sentence


    # model.load_state_dict(torch.load('/content/drive/MyDrive/Ai/ESG_project/study/model_epoch_5.pt'))

    data = [predict_sentence, '0']
    dataset_another = [data]

    another_test = BERTDataset(dataset_another, 0, 1, tok, max_len, True, False) # 토큰화한 문장
    test_dataloader = torch.utils.data.DataLoader(another_test, batch_size = batch_size, num_workers = 5) # torch 형식 변환
    model.eval()

    for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(test_dataloader):
        token_ids = token_ids.long().to(device)
        segment_ids = segment_ids.long().to(device)

        valid_length = valid_length
        label = label.long().to(device)

        out = model(token_ids, valid_length, segment_ids)

        num = 0
        test_eval = []
        for i in out: # out = model(token_ids, valid_length, segment_ids)
            logits = i
            logits = logits.detach().cpu().numpy()

            if np.argmax(logits) == 0:
                test_eval.append("완전 쉣 감정이")
                num = 0
            elif np.argmax(logits) == 1:
                test_eval.append("당췌 엥? 감정이")
                num = 1
            elif np.argmax(logits) == 2:
                test_eval.append("개 좋아! 감정이")
                num = 2

        print(">> 입력하신 내용에서 " + test_eval[0] + " 느껴집니다.")
        return num
    
    import os
import pandas as pd
import re
from IPython.display import clear_output

def str_to_list(s):
    if type(s) != str:
        return -1
    pattern = r'[^a-zA-Z\s]'  # 제거해줄 패턴 : 알파벳이 아닌 것들은 제거
    text = list(set(re.sub(pattern, '', s).split(' ')))  # 리플레이스와 비슷한 것

    if len(text) <= 1:
        return text
    else:
        return [f_str for f_str in text if f_str]
    pass

def f_remove():

    folder_path1 = '/content/drive/MyDrive/Ai/ESG_project/study/sentence_postag'
    folder_path2 = '/content/drive/MyDrive/Ai/ESG_project/study/ESG'

    # 첫 번째 폴더의 파일 목록 가져오기
    comparison_list = os.listdir(folder_path1)

    # 두 번째 폴더의 파일 목록 가져오기
    target_list = os.listdir(folder_path2)
    # print( '첫번째 폴더 : ', len( comparison_list ) )
    # print( '두번째 폴더 : ', len( target_list ) )
    # 중복된 파일 이름 제거
    result_list = [file_name for file_name in comparison_list if file_name not in target_list]

    return result_list

device = torch.device('cpu')
model = BERTClassifier(bertmodel,  dr_rate = 0.5).to(device)
model = torch.load(r'/content/drive/MyDrive/Ai/ESG_project/study/model_5.pt', device)
model.eval()

save_path = '/content/drive/MyDrive/Ai/ESG_project/study/ESG'
folder_path = '/content/drive/MyDrive/Ai/ESG_project/study/sentence_postag'
# Target_list = os.listdir(folder_path)
# print(len(file_list))
file_list = f_remove()
# print(len(file_list))

file_num = 0

for file_idx, file_name in enumerate(file_list[file_num:], start=file_num):

    if '.' not in file_name:  # 파일 이름에 점이 없으면 건너뜁니다.
        continue

    # print( len( df_data['ESG'] ) )
    # if len( df_data['ESG'] ) > 30000:
    #   continue

    file_path = f'{folder_path}/{file_name}'
    # file_path = '/content/drive/MyDrive/Ai/ESG_project/study/sentence_postag/이데일리뉴스_AJ네트웍스.csv'
    df_data = pd.read_csv(file_path)
    df_data['E'] = ''
    df_data['S'] = ''
    df_data['G'] = ''
    df_data['ESG'] = df_data['ESG'].apply(str_to_list)
    max_num = len(df_data['ESG'])

    if max_num > 30000:
      continue

    for index, row in df_data.iterrows():
        if type(row['ESG']) != list:
            continue

        clear_output(wait=True)
        print(f'{file_idx} / {len(file_list)} : {file_name} 시작')
        print(f'{index}/{max_num}')
        print( row['sentence'] )
        num = predict(row['sentence'])

        for f_num in row['ESG']:
            df_data.at[index, f_num] = num

    temp_path = f'{save_path}/{file_list[file_idx]}'
    df_data.to_csv(temp_path, index=False)
    print(f'{file_list[file_idx]} 파일 저장 끝')
    # clear_output(wait=True)
    # break
