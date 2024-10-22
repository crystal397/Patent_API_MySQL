import requests
import xml.etree.ElementTree as ET
import pandas as pd
import time
import os
from dotenv import load_dotenv

load_dotenv()
def get_corp_bs_applicant_info(business_registration_number, access_key):
    url = "http://plus.kipris.or.kr/openapi/rest/CorpBsApplicantService/corpBsApplicantInfoV3"
    params = {
        'BusinessRegistrationNumber': business_registration_number,
        'accessKey': access_key
    }

    for attempt in range(3):  # 최대 3회 시도
        try:
            response = requests.get(url, params=params)

            if response.status_code == 200:
                root = ET.fromstring(response.content)
                result_code = root.find('.//resultCode')
                result_msg = root.find('.//resultMsg')

                result_code = result_code.text if result_code is not None and result_code.text else '00'
                result_msg = result_msg.text if result_msg is not None else "정보 없음"

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
                    return None, None, None, f"오류 코드: {result_code}, 메시지: {result_msg}"
            else:
                return None, None, None, f"API 요청 실패: {response.status_code}"

        except requests.exceptions.RequestException as e:
            if attempt < 2:  # 마지막 시도가 아닐 때만 대기
                time.sleep(3)  # 3초 대기
            else:
                return None, None, None, f"요청 오류: {e}"

# 엑셀 파일에서 사업자등록번호를 불러오기
input_file = 'corporation_numbers.xlsx'
try:
    df = pd.read_excel(input_file)
except Exception as e:
    print(f"엑셀 파일을 열 수 없습니다: {e}")
    exit()

# 'corp_no'라는 열에서 사업자등록번호를 가져오기
business_registration_numbers = df['biz_no'].dropna().tolist()

# 사업자등록번호 형식 변환 및 하이픈 추가
formatted_business_registration_numbers = []
invalid_numbers = []  # 유효하지 않은 사업자등록번호를 보관할 리스트
for num in business_registration_numbers:
    num_str = str(num).strip()
    if len(num_str) == 10:
        formatted_business_registration_numbers.append(f"{num_str[:3]}-{num_str[3:5]}-{num_str[5:]}")
    else:
        invalid_numbers.append(num_str)  # 유효하지 않은 번호 저장
        formatted_business_registration_numbers.append(None)

# 접근 키 입력
access_key = os.getenv('SERVICE_KEY')

# 결과를 저장할 리스트
applicant_numbers = []
applicant_names = []
corporation_numbers = []
failed_requests = []

# 시작 시간 기록
start_time = time.time()

# 각 사업자등록번호에 대해 출원인 정보 조회
for business_registration_number in formatted_business_registration_numbers:
    applicant_number, applicant_name, corporation_number, error_message = get_corp_bs_applicant_info(business_registration_number, access_key)

    if applicant_number:
        applicant_numbers.append(applicant_number)
        applicant_names.append(applicant_name)
        corporation_numbers.append(corporation_number)
    else:
        applicant_numbers.append(None)  # 오류 시 None 추가
        applicant_names.append(None)
        corporation_numbers.append(None)
        print(f"사업자등록번호: {business_registration_number} - 오류: {error_message}")

    # 요청 간 대기 시간 추가
    time.sleep(1)  # 1초 대기

# 종료 시간 기록
end_time = time.time()
execution_time = end_time - start_time

# 결과를 데이터프레임에 추가
df['ApplicantNumber'] = applicant_numbers
df['ApplicantName'] = applicant_names
df['CorporationNumber'] = corporation_numbers

# 결과를 엑셀 파일에 저장
output_file = 'business_registration_results.xlsx'
df.to_excel(output_file, index=False)

# 유효하지 않은 사업자등록번호와 그 총 개수 출력
print(f"결과가 {output_file}에 저장되었습니다.")
print(f"총 소요 시간: {execution_time:.2f}초")

if invalid_numbers:
    print("유효하지 않은 사업자등록번호:")
    for number in invalid_numbers:
        print(number)
    print(f"유효하지 않은 사업자등록번호 총 개수: {len(invalid_numbers)}")
else:
    print("모든 사업자등록번호가 유효합니다.")