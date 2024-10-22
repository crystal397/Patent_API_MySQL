import requests
import xml.etree.ElementTree as ET
import os
from dotenv import load_dotenv

load_dotenv()

def get_corp_bs_applicant_info(business_registration_number, access_key):
    url = "http://plus.kipris.or.kr/openapi/rest/CorpBsApplicantService/corpBsApplicantInfoV3"
    params = {
        'BusinessRegistrationNumber': business_registration_number,
        'accessKey': access_key
    }

    response = requests.get(url, params=params)

    #print(f"요청 URL: {response.url}")  # 요청한 URL 출력
    #print(f"HTTP 상태 코드: {response.status_code}")  # 상태 코드 출력

    if response.status_code == 200:
        #print("응답 내용:", response.content.decode())  # XML 응답 내용 출력

        root = ET.fromstring(response.content)
        result_code = root.find('.//resultCode')
        result_msg = root.find('.//resultMsg')

        # 결과 코드와 메시지 확인
        if result_code is not None and result_code.text:
            result_code = result_code.text
        else:
            result_code = '00'  # 비어있으면 성공으로 간주

        if result_msg is not None:
            result_msg = result_msg.text
        else:
            result_msg = "정보 없음"

        #print(f"결과 코드: {result_code}, 결과 메시지: {result_msg}")  # 결과 코드와 메시지 출력

        if result_code == '00':  # 성공적인 요청
            applicant_info = root.find('.//corpBsApplicantInfo')
            if applicant_info is not None:
                applicant_number = applicant_info.find('ApplicantNumber').text
                applicant_name = applicant_info.find('ApplicantName').text
                corporation_number = applicant_info.find('CorporationNumber').text
                return applicant_number, applicant_name, corporation_number, business_registration_number
            else:
                return None, None, None, "출원인 정보 없음"
        else:
            return None, None, None, result_msg
    else:
        return None, None, None, f"API 요청 실패: {response.status_code}"


# 직접 입력할 사업자등록번호 리스트
business_registration_numbers = [
    '202-81-45602',  # 테스트용 사업자등록번호(홈페이지 샘플 결과값에 보여지는 사업자등록번호)
     # 추가 사업자등록번호를 여기에 입력
]

# 접근 키를 코드에 직접 입력
access_key = os.getenv('SERVICE_KEY')  # 접근 키 입력

# 정보를 저장할 리스트
applicant_numbers = []
applicant_names = []
corporation_numbers = []

# 각 사업자등록번호에 대해 출원인 정보 조회
for business_registration_number in business_registration_numbers:
    applicant_number, applicant_name, corporation_number, _ = get_corp_bs_applicant_info(business_registration_number,
                                                                                         access_key)

    if applicant_number:
        applicant_numbers.append(applicant_number)
        applicant_names.append(applicant_name)
        corporation_numbers.append(corporation_number)

    else:
        applicant_numbers.append(None)  # 오류 시 None 추가
        applicant_names.append(None)
        corporation_numbers.append(None)
        print(f"사업자등록번호: {business_registration_number} - 오류: {applicant_name}")

# 결과 출력
for i in range(len(business_registration_numbers)):
    print(f"사업자등록번호: {business_registration_numbers[i]}, "
          f"특허고객번호: {applicant_numbers[i]}, "
          f"출원인명: {applicant_names[i]}, "
          f"법인번호: {corporation_numbers[i]}")
