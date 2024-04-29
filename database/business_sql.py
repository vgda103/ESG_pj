import pymysql
import configparser
import pandas as pd
# from utility.utility import utility as util

import os
import json

class utility:

    # 경로의 파일이름을 가저와서 get_str 비교하여 원하는 이름 목록을 얻는다
    @staticmethod
    def get_folder_dir( path, get_str ) -> list:
        """
        경로의 파일들을 가져와 get_str 과 비교하여 get_str 문자가 들어있는 파일이름만 가저옴
        path : 가저올 폴더 경로
        get_str : 파일에서 찾을 문자열 ex : '.txt'
        return : list 형 문자열
        """
        # 폴더의 파일 리스트를 가져온다
        li_file = os.listdir( path )

        # 결과를 저장할 변수
        search = []

        # 피일 리스트 만큼 반복
        for file in li_file:

            # get_str 이 li_file 포함 되어 있으면 True
            if get_str in file:

                # 빈 리스트에 추가
                search.append( file )
                pass # if get_str 끝

        # 저장된 리스트를 반환
        return search
        pass # get_folder_dir 끝


    # json 파일을 읽어온다
    @staticmethod
    def read_json( path, encod_num=0 ) -> dict:
        """ 
        path : 파일 경로와 이름을 받아서 json 파일을 읽어 딕셔너리 타입으로 반환
        encod : 사용할 인코더, int 숫자값 0, 1 중 하나 기본값 = 0, 옵션값 : 0 = utf-8, 1 = 'cp949'
        return : 딕셔너리
        """
        encod = [ 'utf-8', 'cp949' ]
        if encod_num < 0 or encod_num > len( encod ):
            return '옵션 범위 밖'

        # JSON 파일 경로
        file_path = path

        # 파일 열기
        with open(file_path, 'r', encoding=encod[ encod_num ] ) as file:
            # data = json.load(file)

            # 파일의 읽고 데이터를 반환
            return json.load(file)

            # 읽어온 데이터를 반환
            # return data
        pass # read_json 끝

    
    # 읽어온 문장 모음을 JSON 파일로 저장
    @staticmethod
    def save_json( path, data, mode_num = 0, encod_num=0 ) -> None:
        """ 
        path : 저장할 경로와 파일 이름
        data : 저장할 데이터. dict 타입
        mode_num : 저장할 옵션, int 숫자값 0, 1 중 하나 기본값 = 0,  옵션값 : 0 = w, 1 = 'a'
        encod : 사용할 인코더, int 숫자값 0, 1 중 하나 기본값 = 0, 옵션값 : 0 = utf-8, 1 = 'cp949'
        """
        encod = [ 'utf-8', 'cp949' ]
        mode = [ 'w', 'a' ]
        if encod_num < 0 or encod_num > len( encod ):
            return '옵션 범위 밖'

        # JSON 파일 저장
        with open( path, mode[ mode_num ], encoding=encod[ encod_num ] ) as file:
            json.dump( data, file, ensure_ascii=False, indent=4)
        pass # save_json 끝
    

    @staticmethod
    def save_file( path, data, mode_num = 0, encod_num=0 ) -> None:
        """
        파일저장, 파일 경로 와 이름
        path : 파일 경로 와 이름, 이름뒤 확장자 넣어야 함
        mode_num : 저장할 옵션, int 숫자값 0, 1 중 하나 기본값 = 0,  옵션값 : 0 = w, 1 = 'a'
        data : 저장할 데이터
        encod : int 숫자값 0, 1 중 하나 기본값 = 0, 옵션값 : 0 = utf-8, 1 = 'cp949'
        """
        encod = [ 'utf-8', 'cp949' ]
        mode = [ 'w', 'a' ]
        if encod_num < 0 or encod_num > len( encod ):
            return '옵션 범위 밖'

        # 예외 처리문
        try:
            # 파일 열기 
            with open( path, mode[ mode_num ], encoding=encod[ encod_num ] ) as txt_f:
                txt_f.write( data ) # txt 파일 저장
        # 파일을 못찾았을 경우 에러 처리
        except FileNotFoundError:
            print(f"File { path } not found.")
        # 예상치 못한 에러를 처리 하는 곳
        except Exception as e:
            print(f"An error occurred while processing { path }: {e}")
        # 정상 작동시 처리되는 곳
        # else:
        #     print( 'txt 변환' )
            pass
        pass # save_file 끝

    @staticmethod
    def open_file( path, encod_num=0 ) -> str:
        """
        파일열기 반환은 str
        path : 파일경로, 파일이름 까지
        encod : int 숫자값 0, 1 중 하나 기본값 = 0, 옵션값 : 0 = utf-8, 1 = 'cp949'
        return : str 
        """
        encod = [ 'utf-8', 'cp949' ]
        if encod_num < 0 or encod_num > len( encod ):
            return '옵션 범위 밖'

        # 예외 처리문
        try:
            # 파일 열기 
            with open( path, 'r', encoding=encod[ encod_num ] ) as txt_f:
                return txt_f.read()
        # 파일을 못찾았을 경우 에러 처리
        except FileNotFoundError:
            print(f"File { path } not found.")
        # 예상치 못한 에러를 처리 하는 곳
        except Exception as e:
            print(f"An error occurred while processing { path }: {e}")
        # 정상 작동시 처리되는 곳
        # else:
        #     print( 'txt 변환' )
            pass
        return 
        pass # open_file 끝
    
    @staticmethod
    def is_float(s) -> bool:
        """
        해당 변수가 float 형인지 아닌지 알려준다 
        return : float 형이면 True, 다른 타입 False
        """
        try:
            float( s )
            return True
        except ValueError:
            return False
        pass # def is_float 끝
    
    pass # class utility 끝


# config open
config = configparser.ConfigParser()
config.read(r'C:\Users\SDA12\Desktop\AiWork\project02\esg\esgpjt-2\config\config.ini')

conn = pymysql.connect(           
            # Local DB
            host = config['DB_TEST']['HOST'],
            port = 3306,
            user = config['DB_TEST']['USER'],
            password = config['DB_TEST']['PASSWD'],
            db = config['DB_TEST']['DB_NAME'],

            #autocommit = True,           
            charset = 'utf8mb4',
            # cursorclass = pymysql.cursors.DictCursor # DB조회시 컬럼명을 동시에 보여줌
        )

# conn = pymysql.connect( 
#     host = 'localhost', # 어떤 컴퓨터에 있는 데이터베이스에 접속 할 것인지
#     # 사용자 계정
#     user = '',
#     # 비밀번호
#     password = '', # secret 파일을 열어서, 읽은 뒤 앞 뒤 공백 삭제
#     database = 'esg_db', # 사용할 데이터베이스
#     charset = 'utf8mb4'
#  )

# 특정 SQL 문을 실행할 때 가져와야되는 것 -> cursor
with conn.cursor() as cursor:
    # 여기서 SQL 문 실행
    
    # 테이블 삭제
    sql = """DROP TABLE IF EXISTS tb_dart_employee;"""
    cursor.execute(sql)

    # 테이블 삭제
    sql = """DROP TABLE IF EXISTS tb_dart_director;"""
    cursor.execute(sql)
    
    # 테이블 삭제
    sql = """DROP TABLE IF EXISTS tb_dart_stock;"""
    cursor.execute(sql)

    # 테이블 목록을 가져온다
    sql = """show tables;"""

    cursor.execute(sql)
    tables = cursor.fetchall() # 실행 결과를 다 가져온다

    
    # # 테이블 삭제
    # sql = """DROP TABLE IF EXISTS students, tb_dart_director, tb_dart_employee, tb_dart_stock;"""
    # cursor.execute(sql)

    # tb_keyword 테이블의 정보를 모두 가져온다.
    sql = """
    SELECT * FROM tb_keyword
     """
    cursor.execute( sql )
    td_keyword = cursor.fetchall()   
        
    # tb_company 테이블의 정보를 모두 가져온다.
    sql = """SELECT COUNT(*) FROM tb_company;"""
    cursor.execute(sql)
    # 열의 수를 가져온다
    max_count = cursor.fetchall()[0][0] # 실행 결과를 다 가져온다
    
    # tb_company 테이블의 정보를 모두 가져온다.
    sql = """
    SELECT * FROM tb_company
     """
    cursor.execute( sql )
    tb_data = cursor.fetchall()    
    
    # tb_keyword 테이블의 정보를 모두 가져온다.
    sql = """
    SELECT * FROM tb_keyword
     """
    cursor.execute( sql )
    df_keyword = pd.DataFrame( cursor.fetchall()  )

    # 가저온 db의 정보를 데이터 프레임으로 저장
    df_data = pd.DataFrame( tb_data )
    di_copr = utility.read_json( 'di_coper.json' )

    keyword = '지역경제'  # 가져오고 싶은 2열의 문자열 값
    emp_key = df_keyword.loc[ df_keyword[2] == keyword, 0 ].iloc[0]
    # print( emp_key )
    
    keyword = '경영안정성'  # 가져오고 싶은 2열의 문자열 값
    director_key = df_keyword.loc[ df_keyword[2] == keyword, 0 ].iloc[0]
    # print( director_key )

    li_employee = []
    li_director = []
    li_stock = []

    for index, row in df_data.iterrows():
        # print( row[ 1 ] )
        # 기업번호, 키워드코드, 총직원수, 정규직수, 비정규직수, 총급여,
        # 전체근속일수, 평균근속연수, 평균급여

        # li_emp = []

        if di_copr.get(row[1], 0):
            if not di_copr[row[1]]['emp_cnt'] == None:
                temp = "{:.2f}".format(round(di_copr[row[1]]['work_day'], 3))
                temp = float(temp)
                li_emp = [ 
                    emp_key,                       # key_code, 키워드 코드, 0
                    row[0],                     # company_seq, 기업번호, 1
                    di_copr[row[1]]['emp_cnt'],    # emp_cnt, 총직원수, 2
                    di_copr[row[1]]['regular_cnt'], # regular_cnt, 정규직, 3
                    di_copr[row[1]]['non_regular_cnt'], # non_regular_cnt, 비정규직, 4
                    di_copr[row[1]]['salary_total'],    # salary_total, 총급여, 5
                    temp,        # work_day, 전체근속일수, 6
                    di_copr[row[1]]['work_avg'],        # work_avg, 평균근속연수, 7
                    # di_copr[row[1]]['salary_avg']       # 평균급여액
                    #row[1],
                ]
                pass # if not di_copr[row[1]]['emp_cnt']
            else:
                li_emp = [ 
                    emp_key,     # 키워드 코드, 0
                    row[0],   # 기업번호, 1
                    0,     # 총직원수, 2
                    0,     # 정규직, 3
                    0,     # 비정규직, 4
                    0,     # 총급여, 5
                    0,     # 전체근속일수, 6
                    0,     # 평균근속연수, 7
                    # None      # 평균급여액
                    #row[1],
                ]
                pass # 

            if not di_copr[row[1]]['director_seq'] == None:
                if type( di_copr[row[1]]['per_salary_avg'] ) == str:
                    try:
                        temp01 = int(di_copr[row[1]]['per_salary_avg'].replace(",", ""))
                        pass # try: 끝
                    except:
                        temp01 = 0
                        pass # except: 끝
                    try:
                        temp02 = int(di_copr[row[1]]['director_salary_total'].replace(",", ""))
                        pass # try: 끝
                    except:
                        temp02 = 0
                        pass # except: 끝
                    pass # if type( di_copr[row[1]]['per_salary_avg'] )
                else:
                    temp01 = di_copr[row[1]]['per_salary_avg']
                    temp02 = di_copr[row[1]]['director_salary_total']
                    pass # else: 끝
                
                li_dir = [
                    director_key,   # key_code, 키워드 코드
                    row[0],         # company_seq, 기업번호
                    di_copr[row[1]]['director_seq'], # director_cnt, 임원수
                    di_copr[row[1]]['out_director_cnt'], # out_director_cnt, 사외이사 수
                    di_copr[row[1]]['in_director_cnt'], # in_director_cnt, 사내이사 수
                    temp01, # per_salary_avg, 1인 평균 급여
                    temp02, # salary_total, 전체 급여
                    # row[1]
                ]
                pass # if not di_copr[row[1]]['director_seq']
            else:
                li_dir = [
                director_key,   # key_code, 키워드 코드
                row[0],         # company_seq, 기업번호
                0, # director_cnt, 임원수
                0, # out_director_cnt, 사외이사 수
                0, # in_director_cnt, 사내이사 수
                0, # per_salary_avg, 1인 평균 급여
                0, # salary_total, 전체 급여
                     ]
                pass # else 끝

            
            if not di_copr[row[1]]['top_stock_percent'] == None:

                li_sok = [
                    director_key,   # key_code, 키워드 코드
                    row[0],         # company_seq, 기업번호
                    di_copr[row[1]]['top_stock_percent'],
                ]
                pass # if not di_copr[row[1]]['top_stock_percent']
            else:

                li_sok = [
                    director_key,   # key_code, 키워드 코드
                    row[0],         # company_seq, 기업번호
                    0,
                ]
                pass # else: 끝

            pass # if di_copr

        else:
            li_emp = [ 
                emp_key,     # 키워드 코드, 0
                row[0],   # 기업번호, 1
                0,     # 총직원수, 2
                0,     # 정규직, 3
                0,     # 비정규직, 4
                0,     # 총급여, 5
                0,     # 전체근속일수, 6
                0,     # 평균근속연수, 7
                # None      # 평균급여액
                #row[1],
            ]

            li_dir = [
                director_key,   # key_code, 키워드 코드
                row[0],         # company_seq, 기업번호
                0, # director_cnt, 임원수
                0, # out_director_cnt, 사외이사 수
                0, # in_director_cnt, 사내이사 수
                0, # per_salary_avg, 1인 평균 급여
                0, # salary_total, 전체 급여
            ]

            li_sok = [
                director_key,   # key_code, 키워드 코드
                row[0],         # company_seq, 기업번호
                0,
            ]
            pass # else 끝

        li_employee.append( li_emp )
        li_director.append( li_dir )
        li_stock.append( li_sok )
        # break
        pass # for index, row 끝

    # 테이블 생성 SQL 쿼리
    # salary_total의 INT로 다 저장 못함으로 BIGINT UNSIGNED 타입으로 해야 함
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS tb_dart_employee (
        emp_seq INT AUTO_INCREMENT PRIMARY KEY,
        key_code SMALLINT NOT NULL,
        company_seq INT NOT NULL,
        emp_cnt INT DEFAULT 0,
        regular_cnt INT DEFAULT 0,
        non_regular_cnt SMALLINT DEFAULT 0,
        salary_total BIGINT UNSIGNED DEFAULT 0,
        work_day FLOAT DEFAULT 0,
        work_avg FLOAT DEFAULT 0,
        
        FOREIGN KEY (key_code) REFERENCES tb_keyword(key_code),
        FOREIGN KEY (company_seq) REFERENCES tb_company(company_seq)
        )
    """
    # 테이블 생성
    cursor.execute(create_table_sql)

    # 데이터 삽입 SQL 쿼리
    insert_data_sql = """
    INSERT INTO tb_dart_employee (
        key_code,
        company_seq,
        emp_cnt,
        regular_cnt,
        non_regular_cnt,
        salary_total,
        work_day,
        work_avg
        )
        VALUES ( %s, %s, %s, %s, %s, %s, %s, %s )
    """
    # executemany() 메서드를 사용하여 데이터 삽입
    cursor.executemany(insert_data_sql, li_employee)


    # 테이블 생성 SQL 쿼리
    create_table_sql = """
        CREATE TABLE tb_dart_director(
            director_seq INT AUTO_INCREMENT PRIMARY KEY,
            key_code SMALLINT NOT NULL,
            company_seq INT NOT NULL,
            director_cnt SMALLINT DEFAULT 0,
            out_director_cnt SMALLINT DEFAULT 0,
            in_director_cnt SMALLINT DEFAULT 0,
            per_salary_avg BIGINT UNSIGNED DEFAULT 0,
            salary_total BIGINT UNSIGNED DEFAULT 0
            )
    """
    # 테이블 생성
    cursor.execute(create_table_sql)

    # 데이터 삽입 SQL 쿼리
    insert_data_sql = """
    INSERT INTO tb_dart_director (
        key_code,
        company_seq,
        director_cnt,
        out_director_cnt,
        in_director_cnt, 
        per_salary_avg,
        salary_total
        )
        VALUES ( %s, %s, %s, %s, %s, %s, %s )
    """
    # executemany() 메서드를 사용하여 데이터 삽입
    cursor.executemany(insert_data_sql, li_director)
    

    # 테이블 생성 SQL 쿼리
    create_table_sql = """
        CREATE TABLE tb_dart_stock(
            stock_seq INT AUTO_INCREMENT PRIMARY KEY,
            key_code SMALLINT NOT NULL,
            company_seq INT NOT NULL,
            top_stock_percent FLOAT DEFAULT 0,
            create_date DATETIME DEFAULT NOW(),
            update_date DATETIME DEFAULT NOW(),
            
            FOREIGN KEY (key_code) REFERENCES tb_keyword(key_code),
            FOREIGN KEY (company_seq) REFERENCES tb_company(company_seq));
    """
    # 테이블 생성
    cursor.execute(create_table_sql)

    
    # 데이터 삽입 SQL 쿼리
    insert_data_sql = """
    INSERT INTO tb_dart_stock (
        key_code,
        company_seq,
        top_stock_percent
        )
        VALUES ( %s, %s, %s )
    """
    # executemany() 메서드를 사용하여 데이터 삽입
    cursor.executemany(insert_data_sql, li_stock)

    # for i, f_li in enumerate( li_stock ):
    #     print( i )
    #     print( f_li )

    #     sql = f"""
    #         INSERT INTO tb_dart_stock (
    #              key_code,
    #              company_seq,
    #              top_stock_percent
    #             )
    #         VALUES(
    #             { f_li[0] }, { f_li[1] },
    #             { f_li[2] }
    #             )
    #     """
    #     # '0', '1', '2', '3', '4', '5', '6', '7'
    #     cursor.execute( sql )
    #     # break
    #     pass # for i, f_li
    
    # tb_company 테이블의 정보를 모두 가져온다.
    sql = """
    SELECT * FROM tb_dart_employee
     """
    cursor.execute( sql )
    tb_test1 = cursor.fetchall()  
    
    # tb_company 테이블의 정보를 모두 가져온다.
    sql = """
    SELECT * FROM tb_dart_director
     """
    cursor.execute( sql )
    tb_test2 = cursor.fetchall()  
    
    # tb_company 테이블의 정보를 모두 가져온다.
    sql = """
    SELECT * FROM tb_dart_stock
     """
    cursor.execute( sql )
    tb_test3 = cursor.fetchall()  
    pass # with conn.cursor()

# 변경사항을 저장하고 연결 종료
conn.commit()
# DB 연결 해제
conn.close()