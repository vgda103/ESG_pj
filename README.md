# Project : 기업 ESG 평가 및 모니터링 서비스 구축
기간 : 2024.4.1 ~ 2024.4.30
2팀 : 동그라미팀 (양, 유, 이, 이, 허)


■ 최종 목표
- ESG 평가 지표 개발
- 비정형 데이터를 활용한 딥러닝 AI 모델링
- 평가 지표를 활용한 기업 가치 평가


■ 프로젝트 요약


1.데이터 수집

- 데이터 소스 크롤링

    - 감정 점수 자료 : 이데일리 뉴스 https://m.edaily.co.kr/search/news/?source=total&keyword=OO사+환경include=&exclude=&jname=&start=20230101&end=20231231
        - 검색 키워드 : 기업명 + keyword list로 크롤링. 
            - 기업 : KRX ESG 등록 799개 기업 https://esg.krx.co.kr/contents/02/02020000/ESG02020000.jsp
            - 키워드 : E(21개 단어), S(24개 단어), G(17개 단어)   ex..온실가스, 친환경, 일자리우수기업, 유연근무, 공정거래, 횡령

    - 수치 점수 자료 : 
        - 업체별 온실가스 배출량/ 에너지 사용량 (엑셀파일) https://ngms.gir.go.kr:8443/subMain.do?link=/hom/bbs/OGCMBBS021V.xml&menuNo=50900501
        - 업체별 폐기물 배출량/ 환경오염물질 배출량 (csv 파일) https://www.keiti.re.kr/site/keiti/08/10805000000002018092809.jsp
        - 온실가스 배출량∙에너지 사용량 DB / 환경법규 위반 행정처분 DB (OPEN API, 승인필요) https://www.bigdata-environment.kr/user/data_market/list.do#
        - KSA 한국표준협회 수상이력 https://ksaesg.or.kr/p_base.php?action=h_krca#
        - 녹색제품 ( 파일 : 한국산업기술진흥원_녹색기술제품확인현황_20230720.csv ) https://www.greencertif.or.kr/ptl/sProductC/form.do
        - 직장어린이집 현황 ( 파일 : 근로복지공단_전국 직장어린이집 현황_20221231.CSV ) https://www.data.go.kr/data/3044314/fileData.do 
        - Dart 사업보고서, 제무제표, 지분공시, 분기보고서,(외부)감사보고서 https://dart.fss.or.kr 
        - KRX ESG 포털 (대기업) 지속 가능 경영 보고서 (https://esg.krx.co.kr/contents/02/02030000/ESG02030000.jsp), 
        - 기업지배구조보고서 (https://esg.krx.co.kr/contents/02/02040000/ESG02040000.jsp)
        - KRX 기업 ESG평가 정보 http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020201
        
- 데이터셋

    - 감정 학습 데이터 : 금융 뉴스 문장 감성 분석 데이터셋 (finance sentiment corpus)
        - 출처 : Finance Phrase Bank (Malo et al., 2014)
        - 데이터 건수 : 4,846건 (금융 뉴스 데이터에서 문장 추출)
        - 감정 라벨 : Positive, Neutral, Negative (16명의 전문지식을 갖춘 연구자들에 의해 수동 라벨링)

        - <도표1> 금융 뉴스 문장 감성 분석 데이터셋
        - ![alt text](<모델 감정.PNG>)
        - 경제 용어가 라벨링되어 있어서 금번 프로젝트의 Fine Tuning에 가장 적합한것으로 생각된다

        - 라벨링이 어떻게 분포되어 있는지 보자
        - <도표2> 감정 라벨링 분포
        - ![alt text](<모델 분포.PNG>)
        - 의외로 중립라벨이 많다.. 는 것은? 16명의 전문가가 일일이 수작업으로 라벨링했다는데 
          알아서들 잘 만들었겠지요..?

    - 감정 대상 데이터 : 뉴스 기사
        - 문서 : 184,097 건
        - 문장 : 4,465,548 건 (1개 문서 24개 문장)
        - 단어 : 481,658,221 건의 명사 단어 (평균 108 토큰)

    - 수치 데이터 : 보완 필요




2.뉴스 기사 전처리

- 기사 간추리기 : 기업명과 키워드 검색, 1개 언론사 선택(기사 중복 방지)
- 정규 표현식 : 한글 외 삭제
- 형태소 분석 : Konlpy Kkma 를 이용한 뉴스의 명사 추출 (정규표현식을 사용한 전처리 수행 결과, 유사단아 추출 정확도 차이)
- ESG 관련기사만 선택
    - Word2vec 모델 활용
        - 전체 뉴스에서 ESG키워드별 유사단어 11개 생성

        - <도표3> Word2vec 모델로 키워드 유사 단어 추출
         ![alt text](<모델 유사단어.png>)
        - Konlpy Kkma 형태소 분석하여 명사만 추출된 토큰에서 유사단어 추출함

        - 뉴스에서 유사단어 없는 문장 제외




3.데이터베이스 구축

- ESG DB구축 
    - 14개 데이블 생성 (기업, 키워드, 뉴스, 수치 자료 등)
     ![alt text](<모델 이알디.PNG>)




4.모델링 & 등급 산정

- 등급 산정을 위한 ESG 배점 전략
    - 데이터 소스별 배점 
        - 총점 100점 ( 감성점수 총75점 : E-25, S-25, G-25  ±  수치 자료의 점수25점) 

- 모델
    - KoBERT 모델 : SKT에서 공개한 한국어 특화 모델 사용 
        - 출처 : 깃허브 SKTBrain (git+https://github.com/SKTBrain/KoBERT.git#egg=kobert_tokenizer&subdirectory=kobert_hf)

- 파인 튜닝
    - 감정 사전 : 라벨링 된 금융 뉴스 문장 감성 분석 데이터셋 (finance_data.csv)
        - 학습 : 3634
        - 테스트 : 1212
        - 감정 클래스 : 3

    - 정확도 (epoch : 5)
        - 학습 : 96.7 %
        - 테스트 : 84.6 % 

        - <도표5> 학습 반복 횟수별 정확도
         ![alt text](<모델 정확도.PNG>)
        - 그래프를 보니 학습 더 시켜봤자 정확도가 크게 올라갈것 같지는 않고..반복 5회 종료
          그런데 테스트 데이터 평가가 약 85 % 로 살짝 걱정이 됨

        - 추가 수작업에 의한 모델 정확도 : 100 % (뉴스 문장으로 20건 Eye Checking)

        - <도표6> 수작업 문장 테스트 
         ![alt text](<모델 확인.PNG>)
        - 감정 라벨링이 필요한 뉴스의 문장을 대입해보니 의외로 정확도가 높았다 100% !!



- 기업별 ESG 점수 산출
    - Word2vec으로 ESG구분된 뉴스 문장별 감정분류 라벨링
        - Positive : + 1
        - Neutral : 0
        - Negative : - 1
        - 라벨링된 감정을 기업별로 ESG 구분하여 누적

        - 여기부터 GPU가 말을 안들어서 그만할래..

# 요기까지 ..
- 이담 부터는 "이렇게 하려고 했다" 임       





    - 수치자료
        - ESG관련 수상, 등록 기업 가점 필요

- 기업 ESG평가 : 점수 분포를 고려한 등급 산정 필요 
    
- 평가 검증 : KRX 기업 ESG평가 결과와 상호 비교 필요




5.시각화 & 파이프라인 구축 필요

- 시각화 : Tableau 를 이용한 대시보드

    - <도표7> 어느 모 기업의 ESG점수
     ![alt text](<모델 막대.PNG>) 
     ![alt text](<모델 스파이더-1.PNG>)
    - 이런식의 그래프로 표현하려고 계획했다.. 계획만 ㅠ

- 데이터 파이프라인 구축...은 언감생심..
    - 실시간 데이터 처리, 분석 파이프라인



6.필요 기술 Set

- 개발환경
    - Python 3.10.x
    - MariaDB 10.6.x
    - 애플리케이션 구축/테스트/배포 소프트웨어 플랫폼 Docker

- 소스코드 관리 : 깃허브

- 업무진행관리 : 노션


7.일정

- 데이터 수집 (1주차)
- 데이터 전처리 (2주차)
- 데이터베이스 구축 (2주차)
- 모델링 & 등급 산정 (3주차)
- 시각화 & 파이프라인 구축 (4주차)
- 프로젝트 정리 (5주차)