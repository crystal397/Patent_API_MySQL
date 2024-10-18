import requests
import xml.etree.ElementTree as ET
import os
from dotenv import load_dotenv

load_dotenv()

def get_patent_info(service_key, params):
    url = "http://plus.kipris.or.kr/kipo-api/kipi/designInfoSearchService/getAdvancedSearch"

    # 파라미터를 딕셔너리로 변환
    request_params = {
        'ServiceKey': service_key,
        'applicantName': params.get('applicantName'),
        'open': params.get('open'),
        'rejection': params.get('rejection'),
        'destroy': params.get('destroy'),
        'cancle': params.get('cancle'),
        'notice': params.get('notice'),
        'registration': params.get('registration'),
        'invalid': params.get('invalid'),
        'abandonment': params.get('abandonment'),
        'simi': params.get('simi'),
        'part': params.get('part'),
        'etc': params.get('etc'),
        'pageNo': params.get('pageNo', 1),  # 기본 페이지 번호
        'numOfRows': params.get('numOfRows', 50),  # 기본 페이지당 건수
        'sortSpec': params.get('sortSpec'),
    }

    # None 값인 파라미터는 제외
    request_params = {k: v for k, v in request_params.items() if v is not None}

    try:
        response = requests.get(url, params=request_params)

        if response.status_code == 200:
            response_content = response.content.decode()
            print("API 응답 XML:\n", response_content)  # XML 구조 확인

            # 응답이 비어있는지 확인
            if not response_content.strip():
                print("응답이 비어 있습니다.")
                return

            # XML 파싱
            root = ET.fromstring(response.content)
            success = root.find('.//successYN').text

            if success == 'Y':
                items = root.findall('.//item')
                if items:
                    for item in items:
                        # 각 항목을 변수에 저장 (None 체크 포함)
                        application_number = item.find('applicationNumber').text if item.find(
                            'applicationNumber') is not None else "없음"
                        application_date = item.find('applicationDate').text if item.find(
                            'applicationDate') is not None else "없음"
                        publication_number = item.find('publicationNumber').text if item.find(
                            'publicationNumber') is not None else "없음"
                        publication_date = item.find('publicationDate').text if item.find(
                            'publicationDate') is not None else "없음"
                        registration_number = item.find('registrationNumber').text if item.find(
                            'registrationNumber') is not None else "없음"
                        registration_date = item.find('registrationDate').text if item.find(
                            'registrationDate') is not None else "없음"
                        priority_number = item.find('priorityNumber').text if item.find(
                            'priorityNumber') is not None else "없음"
                        priority_date = item.find('priorityDate').text if item.find(
                            'priorityDate') is not None else "없음"
                        application_status = item.find('applicationStatus').text if item.find(
                            'applicationStatus') is not None else "없음"
                        applicant_name = item.find('applicantName').text if item.find(
                            'applicantName') is not None else "없음"
                        agent_name = item.find('agentName').text if item.find('agentName') is not None else "없음"
                        full_text = item.find('fullText').text if item.find('fullText') is not None else "없음"
                        inventor_name = item.find('inventorName').text if item.find(
                            'inventorName') is not None else "없음"
                        article_name = item.find('articleName').text if item.find('articleName') is not None else "없음"
                        design_main_classification = item.find('designMainClassification').text if item.find(
                            'designMainClassification') is not None else "없음"
                        open_number = item.find('openNumber').text if item.find('openNumber') is not None else "없음"
                        open_date = item.find('openDate').text if item.find('openDate') is not None else "없음"
                        ds_shp_clss_cd = item.find('dsShpClssCd').text if item.find('dsShpClssCd') is not None else "없음"
                        image_path = item.find('imagePath').text if item.find('imagePath') is not None else "없음"
                        image_path_large = item.find('imagePathLarge').text if item.find(
                            'imagePathLarge') is not None else "없음"
                        design_number = item.find('designNumber').text if item.find(
                            'designNumber') is not None else "없음"
                        app_reference_number = item.find('appReferenceNumber').text if item.find(
                            'appReferenceNumber') is not None else "없음"
                        reg_reference_number = item.find('regReferenceNumber').text if item.find(
                            'regReferenceNumber') is not None else "없음"
                        international_register_number = item.find('internationalRegisterNumber').text if item.find(
                            'internationalRegisterNumber') is not None else "없음"
                        international_register_date = item.find('internationalRegisterDate').text if item.find(
                            'internationalRegisterDate') is not None else "없음"

                        # 출력
                        print(f"출원번호: {application_number}")
                        print(f"출원일자: {application_date}")
                        print(f"공고번호: {publication_number}")
                        print(f"공고일자: {publication_date}")
                        print(f"등록번호: {registration_number}")
                        print(f"등록일자: {registration_date}")
                        print(f"우선권주장번호: {priority_number}")
                        print(f"우선권주장일자: {priority_date}")
                        print(f"출원상태: {application_status}")
                        print(f"출원인명: {applicant_name}")
                        print(f"대리인명: {agent_name}")
                        print(f"전문존재유무: {full_text}")
                        print(f"창작자명: {inventor_name}")
                        print(f"디자인물품명칭: {article_name}")
                        print(f"디자인분류코드: {design_main_classification}")
                        print(f"공개번호: {open_number}")
                        print(f"공개일자: {open_date}")
                        print(f"형태분류: {ds_shp_clss_cd}")
                        print(f"이미지경로: {image_path}")
                        print(f"큰이미지경로: {image_path_large}")
                        print(f"디자인일련번호: {design_number}")
                        print(f"출원참조번호: {app_reference_number}")
                        print(f"등록참조번호: {reg_reference_number}")
                        print(f"국제등록번호: {international_register_number}")
                        print(f"국제등록일자: {international_register_date}\n")
                else:
                    print("검색 결과가 없습니다.")
            else:
                result_msg = root.find('.//resultMsg')
                print(f"API 호출 실패: {result_msg.text if result_msg is not None else '알 수 없는 오류'}")
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
            'applicantName': '420110543860',
            'open': 'true',
            'rejection': 'true',
            'destroy': 'true',
            'cancle': 'true',
            'notice': 'true',
            'registration': 'true',
            'invalid': 'true',
            'abandonment': 'true',
            'simi': 'true',
            'part': 'true',
            'etc': 'true',
            'pageNo': 1,
            'numOfRows': 50,
            'sortSpec': 'applicationDate',
        },
        # {
        #     'applicant': ''
        # }
    ]

    # 각 파라미터로 API 호출
    for params in params_list:
        print(f"검색 조건: {params}")
        get_patent_info(service_key, params)