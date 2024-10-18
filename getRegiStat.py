import requests
import xml.etree.ElementTree as ET
import os
from dotenv import load_dotenv

load_dotenv()

def get_patent_info(service_key, params):
    url = "http://plus.kipris.or.kr/kipo-api/kipi/patUtiModInfoSearchSevice/getAdvancedSearch"

    # 파라미터를 딕셔너리로 변환
    request_params = {
        'ServiceKey': service_key,
        'applicationNumber': params.get('applicationNumber'),
        'pageNo': 1,  # 기본 페이지 번호
        'numOfRows': 50,  # 기본 페이지당 건수
    }

    # None 값인 파라미터는 제외
    request_params = {k: v for k, v in request_params.items() if v is not None}

    try:
        response = requests.get(url, params=request_params)

        if response.status_code == 200:
            # XML 파싱
            root = ET.fromstring(response.content)
            success = root.find('.//successYN').text

            if success == 'Y':
                items = root.findall('.//item')
                if items:
                    for item in items:
                        # 각 항목을 변수에 저장
                        invention_title = item.find('inventionTitle').text
                        register_status = item.find('registerStatus').text
                        applicant_name = item.find('applicantName').text
                        application_number = item.find('applicationNumber').text
                        register_number = item.find('registerNumber').text
                        register_date = item.find('registerDate').text
                        ipc_number = item.find('ipcNumber').text
                        application_date = item.find('applicationDate').text
                        open_number = item.find('openNumber').text
                        open_date = item.find('openDate').text
                        publication_number = item.find('publicationNumber').text
                        publication_date = item.find('publicationDate').text
                        drawing = item.find('drawing').text
                        big_drawing = item.find('bigDrawing').text

                        # 출력
                        print(f"발명의명칭: {invention_title}")
                        print(f"등록상태: {register_status}")
                        print(f"출원인: {applicant_name}")
                        print(f"출원번호: {application_number}")
                        print(f"등록번호: {register_number}")
                        print(f"등록일자: {register_date}")
                        print(f"IPC 코드: {ipc_number}")
                        print(f"출원일자: {application_date}")
                        print(f"공개번호: {open_number}")
                        print(f"공개일자: {open_date}")
                        print(f"공고번호: {publication_number}")
                        print(f"공고일자: {publication_date}")
                        print(f"이미지경로: {drawing}")
                        print(f"큰 이미지경로: {big_drawing}\n")
                else:
                    print("검색 결과가 없습니다.")
            else:
                result_msg = root.find('.//resultMsg').text
                print(f"API 호출 실패: {result_msg}")
        else:
            print(f"HTTP 오류: {response.status_code}")
    except Exception as e:
        print(f"오류 발생: {str(e)}")


# 사용 예시
if __name__ == "__main__":
    service_key = os.getenv('SERVICE_KEY')  # 실제 서비스 키로 변경

    # 미리 정의된 파라미터 리스트
    params_list = [
        {
            'applicationNumber': '1019970062125'
        },
        # {
        #     'applicant': ''
        # }
    ]

    # 각 파라미터로 API 호출
    for params in params_list:
        print(f"검색 조건: {params}")
        get_patent_info(service_key, params)
