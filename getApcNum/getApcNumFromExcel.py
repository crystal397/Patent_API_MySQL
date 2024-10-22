import requests
import xml.etree.ElementTree as ET
import pandas as pd
import time
import os
from dotenv import load_dotenv

load_dotenv()

def get_corp_bs_applicant_info(corporation_number, access_key):
    url = "http://plus.kipris.or.kr/openapi/rest/CorpBsApplicantService/corpBsApplicantInfoV2"
    params = {
        'CorporationNumber': corporation_number,
        'accessKey': access_key
    }

    for attempt in range(11):  # 최대 11회 시도
        try:
            response = requests.get(url, params=params)

            if response.status_code == 200:
                root = ET.fromstring(response.content)
                result_code = root.find('.//resultCode')
                result_msg = root.find('.//resultMsg')

                if result_code is not None and result_code.text:
                    result_code = result_code.text
                else:
                    result_code = '00'

                if result_code == '00':
                    applicant_info = root.find('.//corpBsApplicantInfo')
                    if applicant_info is not None:
                        applicant_number = applicant_info.find('ApplicantNumber').text
                        applicant_name = applicant_info.find('ApplicantName').text
                        return applicant_number, applicant_name, corporation_number
                    else:
                        return None, None, "출원인 정보 없음"
                else:
                    return None, None, f"오류 코드: {result_code}, 메시지: {result_msg}"
            else:
                return None, None, f"API 요청 실패: {response.status_code}"

        except requests.exceptions.RequestException as e:
            if attempt < 2:  # 마지막 시도가 아닐 때만 대기
                time.sleep(3)  # 3초 대기
            else:
                return None, None, f"요청 오류: {e}"


# 엑셀 파일에서 법인번호를 불러오기
input_file = '/Users/a-08/Downloads/corporation_numbers.xlsx'
df = pd.read_excel(input_file)

# 'corp_no'라는 열에서 법인번호를 가져오기
corporation_numbers = df['corp_no'].tolist()
corporation_numbers = [num for num in corporation_numbers if pd.notna(num)]

# 법인번호 형식 변환 및 하이픈 추가
formatted_corporation_numbers = []
invalid_numbers = []  # 유효하지 않은 법인번호를 보관할 리스트
for num in corporation_numbers:
    num_str = str(num).strip()
    if len(num_str) == 13:
        formatted_corporation_numbers.append(f"{num_str[:6]}-{num_str[6:]}")
    else:
        invalid_numbers.append(num_str)  # 유효하지 않은 번호 저장
        formatted_corporation_numbers.append(None)

# 접근 키 입력
access_key = os.getenv('SERVICE_KEY')

# 결과를 저장할 리스트
applicant_numbers = []
applicant_names = []
failed_requests = []

# 시작 시간 기록
start_time = time.time()

# 각 법인번호에 대해 출원인 정보 조회
for index, corporation_number in enumerate(formatted_corporation_numbers):
    if corporation_number:
        applicant_number, applicant_name, error_msg = get_corp_bs_applicant_info(corporation_number, access_key)
        applicant_numbers.append(applicant_number)
        applicant_names.append(applicant_name)
        if applicant_number is None:
            print(f"법인번호: {corporation_number} - 오류: {error_msg}")
            failed_requests.append((index, corporation_number))  # 실패한 요청 기록
    else:
        applicant_numbers.append(None)
        applicant_names.append(None)

    # 요청 간 대기 시간 추가
    time.sleep(1)  # 1초 대기

# 종료 시간 기록
end_time = time.time()
execution_time = end_time - start_time

# 결과를 데이터프레임에 추가
df['ApplicantNumber'] = applicant_numbers
df['ApplicantName'] = applicant_names

# 결과를 엑셀 파일에 저장
output_file = '/Users/a-08/Downloads/business_registration_results.xlsx'
df.to_excel(output_file, index=False)

# 유효하지 않은 법인번호와 그 총 개수 출력
print(f"결과가 {output_file}에 저장되었습니다.")
print(f"총 소요 시간: {execution_time:.2f}초")

if invalid_numbers:
    print("유효하지 않은 법인번호:")
    for number in invalid_numbers:
        print(number)
    print(f"유효하지 않은 법인번호 총 개수: {len(invalid_numbers)}")
else:
    print("모든 법인번호가 유효합니다.")