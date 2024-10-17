import requests
import xml.etree.ElementTree as ET
import os
from dotenv import load_dotenv

load_dotenv()

# API 엔드포인트 URL
url = "http://plus.kipris.or.kr/kipo-api/kipi/patUtiModInfoSearchSevice/getAdvancedSearch"

# 요청 파라미터 설정
params = {
    "astrtCont": "발명",  # 초록
    #"inventionTitle": "센서",  # 발명의 명칭
    "patent": "true",  # 특허 포함 여부
    "utility": "true",  # 실용 포함 여부
    "pageNo": 1,  # 페이지 번호
    "numOfRows": 30,  # 페이지당 건수
    "sortSpec": "PD",  # 정렬 기준 (공고 일자)
    "descSort": "true",  # 정렬 방식 (내림차순)
    "ServiceKey": os.getenv('SERVICE_KEY')  # 인증키
}

# GET 요청 보내기
response = requests.get(url, params=params)

# 응답 상태 코드 확인
if response.status_code == 200:
    # XML 데이터 파싱
    root = ET.fromstring(response.content)

    # XML 출력 (디버깅용)
    print(ET.tostring(root, encoding='utf-8').decode('utf-8'))

    # 요청이 성공했는지 확인
    success = root.find('.//successYN').text
    if success == "Y":
        # 필요한 정보 추출 및 출력
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

            # 모든 정보 출력
            print(f"일련번호: {index_no}")
            print(f"등록상태: {register_status}")
            print(f"발명의 명칭: {invention_title}")
            print(f"IPC 코드: {ipc_number}")
            print(f"등록번호: {register_number}")
            print(f"등록일자: {register_date}")
            print(f"출원번호: {application_number}")
            print(f"출원일자: {application_date}")
            print(f"공개번호: {open_number}")
            print(f"공개일자: {open_date}")
            print(f"공고번호: {publication_number}")
            print(f"공고일자: {publication_date}")
            print(f"초록: {astrt_cont}")
            print(f"이미지 경로: {drawing}")
            print(f"큰 이미지 경로: {big_drawing}")
            print(f"출원인: {applicant_name}")
            print("=" * 40)

            # 이미지 다운로드
            if drawing:
                try:
                    img_response = requests.get(drawing)
                    img_response.raise_for_status()  # 오류 발생 시 예외 발생
                    with open(f"{index_no}_image.jpg", "wb") as img_file:
                        img_file.write(img_response.content)
                    print(f"이미지 {index_no}_image.jpg 다운로드 완료.")
                except Exception as e:
                    print(f"이미지 다운로드 오류: {e}")

            if big_drawing:
                try:
                    big_img_response = requests.get(big_drawing)
                    big_img_response.raise_for_status()
                    with open(f"{index_no}_big_image.jpg", "wb") as big_img_file:
                        big_img_file.write(big_img_response.content)
                    print(f"큰 이미지 {index_no}_big_image.jpg 다운로드 완료.")
                except Exception as e:
                    print(f"큰 이미지 다운로드 오류: {e}")

        # 총 개수 출력
        total_count = root.find('.//totalCount')
        if total_count is not None:
            print(f"총 건수: {total_count.text}")
        else:
            print("총 건수를 찾을 수 없습니다.")
    else:
        print("요청에 실패했습니다.")

else:
    print("오류 발생:", response.status_code)

