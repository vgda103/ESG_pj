import os
import datetime
import getpass
import logging

# 로그 클래스
class Log:
    # 로그 저장
    def log():        
        # LOG 저장 폴더 생성 및 지정
        user_path = r'C:/Users/'
        user_name = getpass.getuser()
        path = user_path+user_name+r'/logs/'

        if os.path.exists(path) == False:
            os.mkdir(user_path+user_name+r'/logs/')

        # 날짜 포멧
        now = datetime.datetime.now()
        formatted_date = now.strftime("%Y-%m-%d")

        # logger instance 설정
        logger = logging.getLogger(__name__)

        # formatter 생성 (로그 출력/저장에 사용할 날짜 + 로그 메시지)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        if logger.hasHandlers(): # 핸들러 존재 여부
            logger.handlers.clear() # 핸들러 삭제

        # handler 생성
        streamHandler = logging.StreamHandler()
        fileHandler = logging.FileHandler(path+f"{formatted_date}.log")

        # logger instance에 formatter 설정
        streamHandler.setFormatter(formatter)
        fileHandler.setFormatter(formatter)

        # logger instance에 handler 추가
        logger.addHandler(streamHandler)
        logger.addHandler(fileHandler)

        # 6. 기록할 log level 지정하기 (LOG LEVEL : DEBUG < INFO < WARNING < ERROR < CRITICAL)
        logger.setLevel(level=logging.DEBUG)
        # logger.setLevel(level=logging.ERROR)                                           

        # 설정된 log setting 반환
        return logger


