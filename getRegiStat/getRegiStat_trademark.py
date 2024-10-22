import requests
import xml.etree.ElementTree as ET
import os
from dotenv import load_dotenv

load_dotenv()

def get_patent_info(service_key, params):
    url = "http://plus.kipris.or.kr/kipo-api/kipi/trademarkInfoSearchService/getAdvancedSearch"

    # 파라미터를 딕셔너리로 변환
    request_params = {
        'ServiceKey': service_key,
        'trademarkName': params.get('trademarkName'),
        'trademarkNameMatch': params.get('trademarkNameMatch'),
        'classification': params.get('classification'),
        'asignProduct': params.get('asignProduct'),
        'applicationNumber': params.get('applicationNumber'),
        'registerNumber': params.get('registerNumber'),
        'publicationNumber': params.get('publicationNumber'),
        'registrationPublicNumber': params.get('registrationPublicNumber'),
        'internationalRegisterNumber': params.get('internationalRegisterNumber'),
        'priorityNumber': params.get('priorityNumber'),
        'applicationDate': params.get('applicationDate'),
        'registerDate': params.get('registerDate'),
        'publicationDate': params.get('publicationDate'),
        'registrationPublicDate': params.get('registrationPublicDate'),
        'internationalRegisterDate': params.get('internationalRegisterDate'),
        'priorityDate': params.get('priorityDate'),
        'applicantName': params.get('applicantName'),
        'agentName': params.get('agentName'),
        'regPrivilegeName': params.get('regPrivilegeName'),
        'viennaCode': params.get('viennaCode'),
        'freeSearch': params.get('freeSearch'),
        'similarityCode': params.get('similarityCode'),
        'application': params.get('application'),
        'registration': params.get('registration'),
        'refused': params.get('refused'),
        'expiration': params.get('expiration'),
        'withdrawal': params.get('withdrawal'),
        'publication': params.get('publication'),
        'cancel': params.get('cancel'),
        'abandonment': params.get('abandonment'),
        'trademark': params.get('trademark'),
        'serviceMark': params.get('serviceMark'),
        'trademarkServiceMark': params.get('trademarkServiceMark'),
        'businessEmblem': params.get('businessEmblem'),
        'collectiveMark': params.get('collectiveMark'),
        'geoOrgMark': params.get('geoOrgMark'),
        'internationalMark': params.get('internationalMark'),
        'certMark': params.get('certMark'),
        'geoCertMark': params.get('geoCertMark'),
        'character': params.get('character'),
        'figure': params.get('figure'),
        'compositionCharacter': params.get('compositionCharacter'),
        'figureComposition': params.get('figureComposition'),
        'sound': params.get('sound'),
        'fragrance': params.get('fragrance'),
        'color': params.get('color'),
        'dimension': params.get('dimension'),
        'colorMixed': params.get('colorMixed'),
        'hologram': params.get('hologram'),
        'motion': params.get('motion'),
        'visual': params.get('visual'),
        'invisible': params.get('invisible'),
        'pageNo': params.get('pageNo', 1),  # 기본 페이지 번호
        'numOfRows': params.get('numOfRows', 30),  # 기본 페이지당 건수
        'sortSpec': params.get('sortSpec'),
        'descSort': params.get('descSort'),
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
                        index_no = item.find('indexNo').text if item.find('indexNo') is not None else "없음"
                        application_number = item.find('applicationNumber').text if item.find(
                            'applicationNumber') is not None else "없음"
                        application_date = item.find('applicationDate').text if item.find(
                            'applicationDate') is not None else "없음"
                        publication_number = item.find('publicationNumber').text if item.find(
                            'publicationNumber') is not None else "없음"
                        publication_date = item.find('publicationDate').text if item.find(
                            'publicationDate') is not None else "없음"
                        registration_public_number = item.find('registrationPublicNumber').text if item.find(
                            'registrationPublicNumber') is not None else "없음"
                        registration_public_date = item.find('registrationPublicDate').text if item.find(
                            'registrationPublicDate') is not None else "없음"
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
                        classification_code = item.find('classificationCode').text if item.find(
                            'classificationCode') is not None else "없음"
                        vienna_code = item.find('viennaCode').text if item.find('viennaCode') is not None else "없음"
                        applicant_name = item.find('applicantName').text if item.find(
                            'applicantName') is not None else "없음"
                        agent_name = item.find('agentName').text if item.find('agentName') is not None else "없음"
                        reg_privilege_name = item.find('regPrivilegeName').text if item.find(
                            'regPrivilegeName') is not None else "없음"
                        title = item.find('title').text if item.find('title') is not None else "없음"
                        full_text = item.find('fullText').text if item.find('fullText') is not None else "없음"
                        drawing = item.find('drawing').text if item.find('drawing') is not None else "없음"
                        big_drawing = item.find('bigDrawing').text if item.find('bigDrawing') is not None else "없음"
                        app_reference_number = item.find('appReferenceNumber').text if item.find(
                            'appReferenceNumber') is not None else "없음"
                        reg_reference_number = item.find('regReferenceNumber').text if item.find(
                            'regReferenceNumber') is not None else "없음"
                        international_register_number = item.find('internationalRegisterNumber').text if item.find(
                            'internationalRegisterNumber') is not None else "없음"
                        international_register_date = item.find('internationalRegisterDate').text if item.find(
                            'internationalRegisterDate') is not None else "없음"

                        # 출력
                        print(f"번호: {index_no}")
                        print(f"출원번호: {application_number}")
                        print(f"출원일자: {application_date}")
                        print(f"출원공고번호: {publication_number}")
                        print(f"출원공고일자: {publication_date}")
                        print(f"등록공고번호: {registration_public_number}")
                        print(f"등록공고일자: {registration_public_date}")
                        print(f"등록번호: {registration_number}")
                        print(f"등록일자: {registration_date}")
                        print(f"우선권주장번호: {priority_number}")
                        print(f"우선권주장일자: {priority_date}")
                        print(f"출원상태: {application_status}")
                        print(f"상품분류코드: {classification_code}")
                        print(f"도형코드: {vienna_code}")
                        print(f"출원인명: {applicant_name}")
                        print(f"대리인명: {agent_name}")
                        print(f"등록권자명: {reg_privilege_name}")
                        print(f"상표명칭: {title}")
                        print(f"전문존재유무: {full_text}")
                        print(f"이미지경로: {drawing}")
                        print(f"큰이미지경로: {big_drawing}")
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
            'ServiceKey': service_key,
            # 'trademarkName': '상표명칭 예시',  # 적절한 값으로 변경 필요
            # 'trademarkNameMatch': 'true',  # 완전일치 여부
            # 'classification': '상품분류코드 예시',  # 적절한 값으로 변경 필요
            # 'asignProduct': '지정상품 예시',  # 적절한 값으로 변경 필요
            # 'applicationNumber': '출원번호 예시',  # 적절한 값으로 변경 필요
            # 'registerNumber': '등록번호 예시',  # 적절한 값으로 변경 필요
            # 'publicationNumber': '출원공고번호 예시',  # 적절한 값으로 변경 필요
            # 'registrationPublicNumber': '등록공고번호 예시',  # 적절한 값으로 변경 필요
            # 'internationalRegisterNumber': '국제등록번호 예시',  # 적절한 값으로 변경 필요
            # 'priorityNumber': '우선권주장번호 예시',  # 적절한 값으로 변경 필요
            # 'applicationDate': '출원일자 예시',  # 적절한 값으로 변경 필요
            # 'registerDate': '등록일자 예시',  # 적절한 값으로 변경 필요
            # 'publicationDate': '출원공고일자 예시',  # 적절한 값으로 변경 필요
            # 'registrationPublicDate': '등록공고일자 예시',  # 적절한 값으로 변경 필요
            # 'internationalRegisterDate': '국제등록일자 예시',  # 적절한 값으로 변경 필요
            # 'priorityDate': '우선권주장일자 예시',  # 적절한 값으로 변경 필요
            'applicantName': '119980018012',
            # 'agentName': '대리인명 예시',  # 적절한 값으로 변경 필요
            # 'regPrivilegeName': '등록권자 예시',  # 적절한 값으로 변경 필요
            # 'viennaCode': '비엔나코드 예시',  # 적절한 값으로 변경 필요
            # 'freeSearch': '자유검색 예시',  # 적절한 값으로 변경 필요
            # 'similarityCode': '유사군코드 예시',  # 적절한 값으로 변경 필요
            'application': 'true',
            'registration': 'true',
            'refused': 'true',
            'expiration': 'true',
            'withdrawal': 'true',
            'publication': 'true',
            'cancel': 'true',
            'abandonment': 'true',
            # 'trademark': 'true',
            # 'serviceMark': 'true',
            # 'trademarkServiceMark': 'true',
            # 'businessEmblem': 'true',
            # 'collectiveMark': 'true',
            # 'geoOrgMark': 'true',
            # 'internationalMark': 'true',
            # 'certMark': 'true',
            # 'geoCertMark': 'true',
            'character': 'true',
            'figure': 'true',
            'compositionCharacter': 'true',
            'figureComposition': 'true',
            'sound': 'true',
            'fragrance': 'true',
            'color': 'true',
            'dimension': 'true',
            'colorMixed': 'true',
            'hologram': 'true',
            'motion': 'true',
            'visual': 'true',
            'invisible': 'true',
            'pageNo': 1,  # 기본 페이지 번호
            'numOfRows': 50,  # 기본 페이지당 건수
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