import requests
import xml.etree.ElementTree as ET
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# MySQL 연결 설정
db_config = {
    'user': 'root',      # MySQL 사용자 이름
    #'password': '',   # MySQL 비밀번호(생략)
    'host': 'localhost',           # MySQL 서버 호스트 (일반적으로 localhost)
    'database': 'PATENT_DB'       # 사용할 데이터베이스 이름
}

# API 엔드포인트 URL
url = "http://plus.kipris.or.kr/kipo-api/kipi/patUtiModInfoSearchSevice/getAdvancedSearch"

# 요청 파라미터 설정
params = {
    "astrtCont": "발명",  # 초록
    "patent": "true",     # 특허 포함 여부
    "utility": "true",    # 실용 포함 여부
    "pageNo": 1,          # 페이지 번호
    "numOfRows": 50,      # 페이지당 건수
    "sortSpec": "PD",     # 정렬 기준 (공고일자)
    "descSort": "true",   # 정렬 방식 (내림차순)
    "ServiceKey": os.getenv('SERVICE_KEY')  # 인증키
}

# GET 요청 보내기
response = requests.get(url, params=params)

# 응답 상태 코드 확인
if response.status_code == 200:
    # XML 데이터 파싱
    root = ET.fromstring(response.content)

    # 요청이 성공했는지 확인
    success = root.find('.//successYN').text
    if success == "Y":
        # MySQL 연결
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # 필요한 정보 추출 및 DB에 저장
        for item in root.findall('.//item'):
            index_no = item.find('indexNo').text
            register_status = item.find('registerStatus').text
            invention_title = item.find('inventionTitle').text
            ipc_number = item.find('ipcNumber').text
            register_number = item.find('registerNumber').text
            register_date = item.find('registerDate').text
            application_number = item.find('applicationNumber').text
            application_date = item.find('applicationDate').text
            open_number = item.find('openNumber').text
            open_date = item.find('openDate').text
            publication_number = item.find('publicationNumber').text
            publication_date = item.find('publicationDate').text
            astrt_cont = item.find('astrtCont').text
            drawing = item.find('drawing').text
            big_drawing = item.find('bigDrawing').text
            applicant_name = item.find('applicantName').text

            # 이미지 다운로드
            # img_data = requests.get(drawing).content if drawing else None
            # big_img_data = requests.get(big_drawing).content if big_drawing else None

            # 데이터베이스에 삽입 (이미지 URL을 저장)
            cursor.execute("""
                            INSERT INTO patents (index_no, register_status, invention_title, ipc_number, register_number, 
                                                 register_date, application_number, application_date, open_number, 
                                                 open_date, publication_number, publication_date, astrt_cont, 
                                                 drawing, big_drawing, applicant_name)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """, (index_no, register_status, invention_title, ipc_number, register_number,
                              register_date, application_number, application_date, open_number,
                              open_date, publication_number, publication_date, astrt_cont,
                              drawing, big_drawing, applicant_name))

            print(f"{invention_title} 정보가 데이터베이스에 저장되었습니다.")

        # 변경 사항 커밋 및 연결 종료
        conn.commit()
        cursor.close()
        conn.close()

        print("모든 데이터가 데이터베이스에 저장되었습니다.")
    else:
        print("요청에 실패했습니다.")
else:
    print("오류 발생:", response.status_code)