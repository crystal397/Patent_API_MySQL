import requests
import xml.etree.ElementTree as ET
import mysql.connector
import time
import os
from dotenv import load_dotenv

load_dotenv()

# MySQL 연결 설정
db_config = {
    'user': 'root',
    # 'password': '',  # MySQL 비밀번호(생략)
    'host': 'localhost',
    'database': 'PATENT_DB'
}

# API 엔드포인트 URL
url = "http://plus.kipris.or.kr/kipo-api/kipi/patUtiModInfoSearchSevice/getAdvancedSearch"

# 요청 파라미터 기본 설정
params = {
    "astrtCont": "발명", # 초록
    "patent": "true",
    "utility": "true",
    "numOfRows": 50,  # 페이지당 건수 설정 (50건)
    "sortSpec": "PD",
    "descSort": "true",
    "ServiceKey": os.getenv('SERVICE_KEY')
}

# MySQL 연결
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

page_no = 1
while True:
    params["pageNo"] = page_no  # 현재 페이지 번호 설정

    # GET 요청 보내기
    response = requests.get(url, params=params)

    # 응답 상태 코드 확인
    if response.status_code == 200:
        root = ET.fromstring(response.content)

        # 요청이 성공했는지 확인
        success = root.find('.//successYN').text
        if success == "Y":
            items = root.findall('.//item')
            if not items:
                break  # 더 이상 데이터가 없으면 종료

            # 필요한 정보 추출 및 DB에 저장
            for item in items:
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

                # 데이터베이스에 삽입
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

            # 변경 사항 커밋
            conn.commit()

            # 1초 대기
            time.sleep(1)
            page_no += 1  # 다음 페이지로 이동
        else:
            print("요청에 실패했습니다.")
            break
    else:
        print("오류 발생:", response.status_code)
        break

# 연결 종료
cursor.close()
conn.close()
print("모든 데이터가 데이터베이스에 저장되었습니다.")
