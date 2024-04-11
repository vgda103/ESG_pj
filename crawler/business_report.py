import time
from IPython.display import clear_output

import dart_fss as dart
from dart_fss.errors import NotFoundConsolidated
# from utility.utility import utility as util
# from utility.Crawling import Crawling

# 만들었던 크롤링 부분을 클레스화?
# 정의
import requests
import json
from bs4 import BeautifulSoup

import os
import json

# Crawling
class Crawling:

    respoonse = None

    def __init__(self) -> None:
        """
        생성자
        """
        self.respoonse = requests
        
        # return self
        pass # 생성자 끝

    def get_requests( self ):
        return self.respoonse


    def url_get( self, URL, headers = {}, data = {}, verify=True ) -> int:
        """
        URL : str, 접속할 사이트주소
        headers : 사이트에서 원하는 해더 타입 입력 기본값은 빈 딕셔너리
        data : 사이트에서 원하는 데이터 타입 기본값은 빈 리스트
        reutnr : int, respoonse 상태를 알려준다.
        """

        # 사이트에 요청
        self.respoonse = requests.get( URL, headers = headers, params = data, verify = verify )
        return self.get_states()        
        pass # 메소드 get_connect
    
    def url_post( self, URL, headers = {}, data = {} ) -> int:
        """
        URL : str, 접속할 사이트주소
        headers : 사이트에서 원하는 해더 타입 입력 기본값은 빈 딕셔너리
        data : 사이트에서 원하는 데이터 타입 기본값은 빈 리스트
        reutnr : int, respoonse 상태를 알려준다.
        """

        # 사이트에 요청
        self.respoonse = requests.post( URL, headers = headers, params = data )
        return self.get_states()        
        pass # 메소드 get_connect

    def get_states( self ) -> int:
        """
        respoonse 상태를 알려준다.
        """
        return self.respoonse.status_code
        pass # get_res_states 

    def get_text( self ) -> str:
        """
        respoonse의 속성의 텍스트를 넘겨준다
        """
        return self.respoonse.text
        pass # get_text 끝

    def get_to_json( self ):
        """
        load를 사용하니 사용하지 말것
        load는 파일에서 읽어올때 사용함
        loads는 문자열을 읽을때 사용함
        respoonse를 json 형태로 파싱한 데이터를 넘겨준다
        """
        # j_data = json.loads( self.respoonse.text )
        return json.load( self.respoonse.text )
        pass # get_to_json 끝
    
    def get_to_jsons( self ):
        """
        loads를 사용함
        load는 파일에서 읽어올때 사용함
        loads는 문자열을 읽을때 사용함
        respoonse를 json 형태로 파싱한 데이터를 넘겨준다
        """
        # j_data = json.loads( self.respoonse.text )
        return json.loads( self.respoonse.text )
        pass # get_to_json 끝
    
    def get_to_soup( self ):
        """
        respoonse를 BeautifulSoup 형태로 파싱한 데이터를 넘겨준다
        """
        return BeautifulSoup( self.respoonse.text, 'html.parser' )
        pass # get_to_soup 끝

    def get_parser( self ):

        get_str = self.respoonse.text[ :100 ]

        if get_str.find( '<!DOCTYPE HTML>' ):
            return self.get_to_soup()
            pass

        elif get_str.find( '{' ):
            return self.get_to_jsons()
        
        else:
            return self.get_text()
            pass
        pass # get_parser 끝

    pass # class Crawling 끝


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

class Business_report( Crawling, utility ):
    
    def __init__(self) -> None:
        """
        생성자
        속성 
        li_c_list : 파일에서 읽어온 사업보고서 회사리스트
        corp_list : 공시된 전체 회사 리스트
        """

        # 파일의 회사 리스트를 메모리에 저장
        self.li_c_list = self.read_json( 'business_report_list.json' )
        
        # Open DART API KEY 설정
        self.api_key = self.open_file( 'api.key' )
        dart.set_api_key(api_key=api_key)

        # DART 에 공시된 회사 리스트 불러오기
        self.corp_list = dart.get_corp_list()
        # self.max_corp = len( self.li_c_list )

        self.num = 0

        pass # def __init__ 끝

    def get_FinancialStatements( self, corp, date = '20230101', path = './Financial_Statements' ) -> None:
        """
        제무제표를 저장한다
        corp : dart 에서 사용하는 회사의 데이터 형식
        date : str, YYYYMMDD 형식의 문자열 날자
        path : 저장할 파일 경로, 클레스기본값 : ./Financial_Statements, dart기본값 : /fsdata
        return : 
            에러시 : dict 형식{ 회사명 : f{에러코드} }
            정상 : None
        """

        # 예외처리
        try:
            # 날짜 부터 연간 연결재무제표 불러오기
            fs = corp.extract_fs(bgn_de=date)
            pass # try 끝

        # try 문 에러시 실행 되는 except
        except NotFoundConsolidated:
            print('연결재무제표가 없으므로 개별재무제표를 추출합니다.')

            # 예외처리
            try:
                # 연결 제무제표가 없을시 실행
                fs = dart.fs.extract( corp.corp_code, bgn_de=date, separate=True) # corp.corp_code 개별재무제표추출
                pass # try 끝

            # try 문 에러시 실행 되는 except
            except Exception as e:  # 모든 예외를 처리하는 except 블록 추가
                
                print(f'예외가 발생했습니다: {e}')
                # 예외가 발생했지만 프로그램을 중단시키지 않고 계속 실행하려면 pass 문을 추가할 수 있습니다.
                # 에러 회사명과 에러코드 리턴
                return { corp.corp_name : f'{e}' }
                pass
        
        # try 후 반드시 실행되는 구간
        finally:
            # 재무제표 검색 결과를 엑셀파일로 저장 ( 기본저장위치: 실행폴더/fsdata )
            file_name = f'{ corp.corp_name }.xlsx'      # 파일 이름 생성
            # 생성된 파일이름과 경로로 저장
            fs.save(file_name, path)
    
        pass # def get_FinancialStatements 끝

    def get_business_data( self, corp, dete = '2023', doc_num = '11011' ) -> ( dict, list ):
        """
        사업보고서 에서 필요한 데이터를 얻어서 반환
        corp : dart 에서 사용하는 회사의 데이터 형식
        date : str, YYYYMMDD 형식의 문자열 날자
        path : 저장할 파일 경로, 클레스기본값 : ./Financial_Statements, dart기본값 : /fsdata
        return : 
            에러시 : dict 형식{ 회사명 : f{에러코드} }
            정상 : dict 형식 데이터
        """
        dic_temp = {}
        error_corp = []

        # test_corp
        # print( test_corp )
        # print( test_corp.corp_name )

        # 테스트 브레이크
        # break

        dic_temp[ 'comp_name' ] = corp.corp_name
        corp_code = corp.corp_code
        
        # dic_temp[ '기업명' ] = corp_list[ i ].corp_name

        ###############################################################################
        # 직원 현황
        ###############################################################################
        try:
            # 직원 현황을 호출후 데이터를 저장
            dic_employee = dart.api.info.emp_sttus( corp_code, dete, doc_num )
            # rgllbr_co : 정규직
            # rgllbr_abacpt_labrr_co : (기간의 정함이 없는)단시간 근로자
            # cnttk_co : 기간제 근로자
            # cnttk_abacpt_labrr_co : 기간제 단시간 근로자
            # avrg_cnwk_sdytrn : 근속 년수
            # sm : 성별 근로자 합
            # fyer_salary_totamt : 연간 급여 총액
            # dic_employee[ 'list' ][-1]

            totla_employee = 0          # 전체 근로자
            Full_time = 0               # 정규직
            # part_time_without_period = 0 # 기간이 없는 단시간 근로자
            # fixed_term = 0              # 기간제 근로자
            part_time = 0               # 단시간 근로자
            # average_service = []        # 평균 근속 년수
            total_average_service = 0   # 총 근속 일수
            # average_pay = []            # 1인 평균 급여
            total_pay = 0               # 전체 급여

            # 마지막 두개 데이터에서 데이터를 가져온다
            for f_num in range( 1, 3 ):
                # 테스트 출력
                # print( dic_employee[ 'list' ][ -i ] )
                # 전체 직원수 누적 저장
                totla_employee += int( dic_employee[ 'list' ][ -f_num ][ 'sm' ].replace( ',', '' ) )
                # 풀타임 근로자 누적 저장
                Full_time += int( dic_employee[ 'list' ][ -f_num ][ 'rgllbr_co' ].replace( ',', '' ) )
                # 파트타임 근로자 누적 저장
                part_time += 0 if dic_employee[ 'list' ][ -f_num ][ 'cnttk_co' ] == '-' else int( dic_employee[ 'list' ][ -f_num ][ 'cnttk_co' ].replace( ',', '' ) )
                # 전체 임금 누적 저장
                total_pay += int( dic_employee[ 'list' ][ -f_num ][ 'fyer_salary_totamt' ].replace( ',', '' ) )
                
                        
                # print( 'for 문 안' )   
                # print( 'avrg_cnwk_sdytrn : ', dic_employee[ 'list' ][ -i ][ 'avrg_cnwk_sdytrn' ] )
                # print( 'rgllbr_co : ', dic_employee[ 'list' ][ -i ][ 'rgllbr_co' ] )
                # print( 'for 문 끝' )

                # avrg_cnwk_sdytrn의 데이터가 float 형으로 형변환이 되는 데이터형인가? 구분
                if self.is_float( dic_employee[ 'list' ][ -f_num ][ 'avrg_cnwk_sdytrn' ] ):
                    # float 형변환 되면 형변환 후 누적 저장
                    # 근로자 근로기간 전체 일수 누적 저장, 근속 년수 * 풀타임 근로자수
                    total_average_service += float( dic_employee[ 'list' ][ -f_num ][ 'avrg_cnwk_sdytrn' ] ) * int( dic_employee[ 'list' ][ -f_num ][ 'rgllbr_co' ].replace( ',', '' ) ) 
                    pass   # if is_float 끝

                else:
                    # float 형으로 형변환이 안되는 데이터
                    # avrg_cnwk_sdytrn 데이터를 메모리에 저장
                    str_temp = dic_employee[ 'list' ][ -f_num ][ 'avrg_cnwk_sdytrn' ]
                    # 문자열에서 필요 없는 문자열 제거 또는 변경
                    str_temp = str_temp.replace( '년', '.' )
                    str_temp = str_temp.replace( '개월', '' )
                    # print( '처리 : ', str_temp )

                    # 근로자 근로기간 전체 일수 누적 저장, 근속 년수 * 풀타임 근로자수
                    total_average_service += float( str_temp ) * int( dic_employee[ 'list' ][ -f_num ][ 'rgllbr_co' ].replace( ',', '' ) ) 
                    pass # if self.is_float else 끝
                pass # for f_num 끝

            # dic_el_datas = []

            # print( '총직원수 : ', totla_employee )                     # 총직원수
            # print( '정규직 : ', Full_time )                          # 정규직
            # print( '비정규직 : ', part_time )                          # 비정규직
            # # print( average_service[0], average_service[1] )
            # print( '총 급여 : ', total_pay )                          # 총 급여
            # print( '전체 근속일수 : ', total_average_service )              # 전체 근속일수
            # print( '평균 근속연수 : ', total_average_service // Full_time )  # 평균 근속연수
            # print( '평균 급여액 : ', total_pay // totla_employee )  

            # 총직원수
            dic_temp[ 'emp_cnt' ] = totla_employee
            # 풀타임근로자
            dic_temp[ 'regular_cnt' ] = Full_time
            # 파트타임 근로자
            dic_temp[ 'non_regular_cnt' ] = part_time
            # 총급여
            dic_temp[ 'salary_total' ] = total_pay
            # 총 근로일수
            dic_temp[ 'work_day' ] = total_average_service
            # 년평균 근로일수 
            dic_temp[ 'work_avg' ] = total_average_service // Full_time
            # 평균 임금
            dic_temp[ 'salary_avg' ] = total_pay // totla_employee
            pass # try 직원 끝

        # 데이터가 없을때 처리
        except:
            print( '직원 없음 넘어감' )

            dic_temp[ 'emp_cnt' ] = 0
            dic_temp[ 'regular_cnt' ] = 0
            dic_temp[ 'non_regular_cnt' ] = 0
            dic_temp[ 'salary_total' ] = 0
            dic_temp[ 'work_day' ] = 0
            dic_temp[ 'work_avg' ] = 0
            dic_temp[ 'salary_avg' ] = 0
            # 에러 목록에 회사명과 에러 난곳을 추가
            error_corp.append( f'[{ dic_temp[ "comp_name" ] }:직원]' )
            pass # except 끝

        # # 테스트 브레이크
        # break

        ###############################################################################
        # 임원 현황 
        ###############################################################################
        # 예외처리
        try:
            # 임원 현환을 호출후 저장
            executives = dart.api.info.exctv_sttus( corp_code, dete, doc_num )
            # executives[ 'list' ]
            outside_company = 0     # 사외이사 수
            company = 0             # 사내이사 수

            # executives[ 'list' ]의 rgist_exctv_at 에서 사외 라는 단어가 있으면 카운터후 합
            outside_company = sum( [ 1 for item in executives[ 'list' ] if '사외' in item[ 'rgist_exctv_at' ] ] )
            # 사내이사 를 계산
            company = len( executives[ 'list' ] ) - outside_company

            # print( '전체임원수 : ', len( executives[ 'list' ] ) )
            # print( '사외이사 : ', outside_company )
            # print( '사내이사 : ', company )
            # print( '사외이사비율 : ', outside_company // len( executives[ 'list' ] ) * 100 ) 

            # 전체 임원수
            dic_temp[ 'director_seq' ] = len( executives[ 'list' ] )
            # 사외이사 수
            dic_temp[ 'out_director_cnt' ] = outside_company
            # 사내이사
            dic_temp[ 'in_director_cnt' ] = company
            # 사외이사 비율
            dic_temp[ 'outside_ratio' ] = outside_company // len( executives[ 'list' ] ) * 100
            pass # try 임원 끝

        # 데이터가 없을때 처리
        except:
            print( '임원 없음 넘어감' )

            dic_temp[ 'director_seq' ] = 0
            dic_temp[ 'out_director_cnt' ] = 0
            dic_temp[ 'in_director_cnt' ] = 0
            dic_temp[ 'outside_ratio' ] = 0
            
            # 에러 목록에 회사명과 에러 난곳을 추가
            error_corp.append( f'[{ dic_temp[ "comp_name" ] }:임원 인원수]' )
            pass # except 임원 끝
        
        
        # # 테스트 브레이크
        # break
        
        ########################################################################################
        # 임원 전체 보수 
        ########################################################################################
        try:
            # 임원 보수 데이터를 가져온다
            di_all_directorate_meed = dart.api.info.hmv_audit_all_sttus( 
                corp_code, dete, doc_num )
            # nmpr : 임원수
            # jan_avrg_mendng_am : 1인당 평균보수액
            # mendng_totamt : 전체 합
            # di_all_directorate_meed[ 'list' ]

            # 임원 1인당 평균 보수액 저장
            # avg_executives_mending = di_all_directorate_meed[ 'list' ][0][ 'jan_avrg_mendng_am' ]
            # 임원 전체 합을 가져온다
            # total_executives_mending = di_all_directorate_meed[ 'list' ][0][ 'mendng_totamt' ]

            # print( '임원1인평균임금 : ', avg_executives_mending )
            # print( '임원총임금 : ', total_executives_mending )


            dic_temp[ 'per_salary_avg' ] = di_all_directorate_meed[ 'list' ][0][ 'jan_avrg_mendng_am' ]
            dic_temp[ 'salary_total' ] = di_all_directorate_meed[ 'list' ][0][ 'mendng_totamt' ]
            pass # try 임원 전체 보수 끝

        # 데이터가 없을때 처리
        except:
            print( '임원 전체보수 없음 넘어감' )

            dic_temp[ 'per_salary_avg' ] = 0
            dic_temp[ 'salary_total' ] = 0

            # 에러 목록에 회사명과 에러 난곳을 추가
            error_corp.append( f'[{ dic_temp[ "comp_name" ] }:임원 전체보수]' )
            pass # except 끝
        
        # # 테스트 브레이크
        # break

        ########################################################################################
        # 최대주주 현황
        ########################################################################################

        # doc_num = '11011'
        
        #DART OPEN API 이용한 url
        URL = 'https://opendart.fss.or.kr/api/hyslrSttus.json?'
        URL += f'crtfc_key={ self.api_key }&corp_code={ corp_code }&bsns_year={ dete }&reprt_code={ doc_num }'

        # 조립된 URL 로 접속
        self.url_get( URL=URL )
        # 접속 데이터를 가져온다
        bulk_stocks = self.get_to_jsons()

        # bulk_stocks[ 'message' ]의 데이터에 조회된 이란 값이 있는지 확인
        if '조회된' in bulk_stocks[ 'message' ]:
            # 데이터가 없을때 처리
            print( '최대주주 현황 없음 넘어감' )

            dic_temp[ 'top_stock_percent' ] = 0
            
            error_corp.append( f'[{ dic_temp[ "comp_name" ] }:최대주주 현황]' )
            # dic_corp_data.append( dic_temp )
            return dic_temp
            pass # if '조회된' 끝
        
        # 데이터가 있을때 처리
        total_stocks = 0.0
        # 마지막 2개의 데이터를 빼고 데이터를 가저온다
        for f_num in range( len( bulk_stocks[ 'list' ] ) - 2 ):

            # 데이터가 - 이면 건너 뛴다
            if bulk_stocks[ 'list' ][ f_num ][ 'trmend_posesn_stock_qota_rt' ] == '-':
                continue

            # 데이터 누적
            # print( bulk_stocks[ 'list' ][ i ][ 'trmend_posesn_stock_qota_rt' ] )
            total_stocks += float( bulk_stocks[ 'list' ][ f_num ][ 'trmend_posesn_stock_qota_rt' ] )
            pass

        # print( '최대주주지분율 : ', total_stocks )
        dic_temp[ 'top_stock_percent' ] = total_stocks

        # 얻은 데이터를 반환
        return dic_temp, error_corp
        pass # def get_business_data 끝

    def test( self ):
        test_corp = self.corp_list.find_by_corp_name( self.li_c_list[ 500 ], exactly=True )[0]
        d = self.get_business_data( test_corp )
        print( d )
        pass

    def connect( self, date = '2023' ) -> None:
        """
        접속하여 사업보고서 데이터와 제무제표를 다운 또는 파일을 저장한다
        직원현황(6항목), 임원현황(6항목), 최대주주현황(1항목)
        date : 데이터를 검색할 년도
        """
        
        MAX_CONNECTIONS_PER_MINUTE = 60     # 총 반복 횟수
        SECONDS_PER_MINUTE = 90             # 한계 시간(분)
        
        max_corp = len( self.li_c_list )    # 전체 수

        doc_num = '11011'                   # 문서 번호
        li_corp_data = []                   # 회사 데이터를 저장할 변수 
        error_corp = []                     # 에러를 저장할 변수
        # num = 0
        index = 0                           # 인덱스

        
        # 이전 접속 시간 초기화
        previous_minute = time.time()       # 현제시간 저장
        connections_this_minute = 0         # 접속 수 카운터
        
        while True:

            # # 테스트 브레이크
            # break

            # 현재 시간 저장
            current_time = time.time()

            # 현재 시간 - 이전 시간의 값이 SECONDS_PER_MINUTE 보다 크면 연결 수 초기화
            if current_time - previous_minute >= SECONDS_PER_MINUTE:
                # 이전시간 초기화
                previous_minute = current_time
                # 접속 수를 초기화
                connections_this_minute = 0 
                # 출력 화면을 클리어
                clear_output(wait=True)
                pass # if current_time - previous_minute 끝

            # 현제 접속 수가 최대 접속 수보다 적은지 확인
            if connections_this_minute < MAX_CONNECTIONS_PER_MINUTE:
                # 여기에 접속 코드 추가
                # print("접속을 합니다.")
                # print( f'{ i } : { connections_this_minute }' )

                # i 가 max_corp 보다 크면, 함수 종료
                if index >= max_corp:
                    print( '모든 회사를 다 돌았음' )
                    break # if i 끝

                # self.corp_list.find_by_corp_name 의 리턴값이 없다면 건너 뛴다
                if not self.corp_list.find_by_corp_name( self.li_c_list[ index ], exactly=True ):
                    error_corp.append( f'[{ self.li_c_list[ index ] }:데이터없음]' )
                    # 회사에 인덱스로 사용할 값 증가            
                    index += 1
                    # 접속 수 증가
                    connections_this_minute += 1
                    continue
                    pass # if not self.corp_list.find_by_corp_name 끝

                # 회사명으로 회사의 데이터를 가저온다.
                corp = self.corp_list.find_by_corp_name( self.li_c_list[ index ], exactly=True )[0]

                # 중간 출력문 : 실행수 / 전체수 : 회사명
                print( f'{ index } / { max_corp } : { corp.corp_name }' )

                data, err = self.get_business_data( corp, dete = date, doc_num = doc_num )

                li_corp_data.append( data )
                error_corp += err

                self.get_FinancialStatements( corp, dete = date, doc_num = doc_num  )

                # print( li_corp_data )
                # print( error_corp )

                # if index > 2:
                #     break

                # break # 테스트 브레이크
                
                # 회사에 인덱스로 사용할 값 증가
                index += 1
                # 접속 수 증가
                connections_this_minute += 1
                
                pass # if connections_this_minute 끝

            else:
                # 최대 접속 수를 초과한 경우 대기
                # clear_output(wait=True)
                print("최대 접속 수를 초과하여 대기합니다.")
                time.sleep(1)  # 1초 대기 후 다시 시도
                pass # else 끝
            
            pass # while 끝
        
        # 파일 저장
        self.save_json( f'coper{ self.num }.json', li_corp_data )
        self.save_json( f'error_coper.json', error_corp )

        self.num += 1

        pass # def connect 끝


    def get_connect_Financial( self, date = '2023' ) -> None:
        """
        접속하여 제무제표 다운받는다
        직원현황(6항목), 임원현황(6항목), 최대주주현황(1항목)
        date : 데이터를 검색할 년도
        """
        
        MAX_CONNECTIONS_PER_MINUTE = 60     # 총 반복 횟수
        SECONDS_PER_MINUTE = 90             # 한계 시간(분)
        
        max_corp = len( self.li_c_list )    # 전체 수

        doc_num = '11011'                   # 문서 번호
        # li_corp_data = []                   # 회사 데이터를 저장할 변수 
        error_corp = []                     # 에러를 저장할 변수
        # num = 0
        index = 0                           # 인덱스

        
        # 이전 접속 시간 초기화
        previous_minute = time.time()       # 현제시간 저장
        connections_this_minute = 0         # 접속 수 카운터
        
        while True:

            # # 테스트 브레이크
            # break

            # 현재 시간 저장
            current_time = time.time()

            # 현재 시간 - 이전 시간의 값이 SECONDS_PER_MINUTE 보다 크면 연결 수 초기화
            if current_time - previous_minute >= SECONDS_PER_MINUTE:
                # 이전시간 초기화
                previous_minute = current_time
                # 접속 수를 초기화
                connections_this_minute = 0 
                # 출력 화면을 클리어
                clear_output(wait=True)
                pass # if current_time - previous_minute 끝

            # 현제 접속 수가 최대 접속 수보다 적은지 확인
            if connections_this_minute < MAX_CONNECTIONS_PER_MINUTE:
                # 여기에 접속 코드 추가
                # print("접속을 합니다.")
                # print( f'{ i } : { connections_this_minute }' )

                # i 가 max_corp 보다 크면, 함수 종료
                if index >= max_corp:
                    print( '모든 회사를 다 돌았음' )
                    break # if i 끝

                # self.corp_list.find_by_corp_name 의 리턴값이 없다면 건너 뛴다
                if not self.corp_list.find_by_corp_name( self.li_c_list[ index ], exactly=True ):
                    error_corp.append( f'[{ self.li_c_list[ index ] }:데이터없음]' )
                    # 회사에 인덱스로 사용할 값 증가            
                    index += 1
                    # 접속 수 증가
                    connections_this_minute += 1
                    continue
                    pass # if not self.corp_list.find_by_corp_name 끝

                # 회사명으로 회사의 데이터를 가저온다.
                corp = self.corp_list.find_by_corp_name( self.li_c_list[ index ], exactly=True )[0]

                # 중간 출력문 : 실행수 / 전체수 : 회사명
                print( f'{ index } / { max_corp } : { corp.corp_name }' )

                self.get_FinancialStatements( corp, dete = date, doc_num = doc_num  )

                # print( li_corp_data )
                # print( error_corp )

                # if index > 2:
                #     break

                # break # 테스트 브레이크
                
                # 회사에 인덱스로 사용할 값 증가
                index += 1
                # 접속 수 증가
                connections_this_minute += 1
                
                pass # if connections_this_minute 끝

            else:
                # 최대 접속 수를 초과한 경우 대기
                # clear_output(wait=True)
                print("최대 접속 수를 초과하여 대기합니다.")
                time.sleep(1)  # 1초 대기 후 다시 시도
                pass # else 끝
            
            pass # while 끝

        pass # def get_connect_Financial 끝


    def get_connect_Business( self, date = '2023' ) -> None:
        """
        접속하여 데이터를 가져온다와서 파일로 저장
        직원현황(6항목), 임원현황(6항목), 최대주주현황(1항목)
        date : 데이터를 검색할 년도
        """
        
        MAX_CONNECTIONS_PER_MINUTE = 60     # 총 반복 횟수
        SECONDS_PER_MINUTE = 90             # 한계 시간(분)
        
        max_corp = len( self.li_c_list )    # 전체 수

        doc_num = '11011'                   # 문서 번호
        li_corp_data = []                   # 회사 데이터를 저장할 변수 
        error_corp = []                     # 에러를 저장할 변수
        # num = 0
        index = 0                           # 인덱스

        
        # 이전 접속 시간 초기화
        previous_minute = time.time()       # 현제시간 저장
        connections_this_minute = 0         # 접속 수 카운터
        
        while True:

            # # 테스트 브레이크
            # break

            # 현재 시간 저장
            current_time = time.time()

            # 현재 시간 - 이전 시간의 값이 SECONDS_PER_MINUTE 보다 크면 연결 수 초기화
            if current_time - previous_minute >= SECONDS_PER_MINUTE:
                # 이전시간 초기화
                previous_minute = current_time
                # 접속 수를 초기화
                connections_this_minute = 0 
                # 출력 화면을 클리어
                clear_output(wait=True)
                pass # if current_time - previous_minute 끝

            # 현제 접속 수가 최대 접속 수보다 적은지 확인
            if connections_this_minute < MAX_CONNECTIONS_PER_MINUTE:
                # 여기에 접속 코드 추가
                # print("접속을 합니다.")
                # print( f'{ i } : { connections_this_minute }' )

                # i 가 max_corp 보다 크면, 함수 종료
                if index >= max_corp:
                    print( '모든 회사를 다 돌았음' )
                    break # if i 끝

                # self.corp_list.find_by_corp_name 의 리턴값이 없다면 건너 뛴다
                if not self.corp_list.find_by_corp_name( self.li_c_list[ index ], exactly=True ):
                    error_corp.append( f'[{ self.li_c_list[ index ] }:데이터없음]' )
                    # 회사에 인덱스로 사용할 값 증가            
                    index += 1
                    # 접속 수 증가
                    connections_this_minute += 1
                    continue
                    pass # if not self.corp_list.find_by_corp_name 끝

                # 회사명으로 회사의 데이터를 가저온다.
                corp = self.corp_list.find_by_corp_name( self.li_c_list[ index ], exactly=True )[0]

                # 중간 출력문 : 실행수 / 전체수 : 회사명
                print( f'{ index } / { max_corp } : { corp.corp_name }' )

                data, err = self.get_business_data( corp, dete = date, doc_num = doc_num )

                li_corp_data.append( data )
                error_corp += err

                # print( li_corp_data )
                # print( error_corp )

                # if index > 2:
                #     break

                # break # 테스트 브레이크
                
                # 회사에 인덱스로 사용할 값 증가
                index += 1
                # 접속 수 증가
                connections_this_minute += 1
                
                pass # if connections_this_minute 끝

            else:
                # 최대 접속 수를 초과한 경우 대기
                # clear_output(wait=True)
                print("최대 접속 수를 초과하여 대기합니다.")
                time.sleep(1)  # 1초 대기 후 다시 시도
                pass # else 끝
            
            pass # while 끝
        
        # 파일 저장
        self.save_json( f'coper{ self.num }.json', li_corp_data )
        self.save_json( f'error_coper.json', error_corp )

        self.num += 1

        pass # def get_connect_Business 끝

    pass # class Business_report 끝