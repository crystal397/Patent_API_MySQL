import requests
import xml.etree.ElementTree as ET
import pandas as pd
import time
import os
from dotenv import load_dotenv

load_dotenv()

# 사업자등록번호 기반 API 호출 함수
def get_corp_bs_applicant_info_br(business_registration_number, access_key):
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

# 법인번호 기반 API 호출 함수
def get_corp_bs_applicant_info(corporation_number, access_key):
    url = "http://plus.kipris.or.kr/openapi/rest/CorpBsApplicantService/corpBsApplicantInfoV2"
    params = {
        'CorporationNumber': corporation_number,
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

                if result_code == '00':
                    applicant_info = root.find('.//corpBsApplicantInfo')
                    if applicant_info is not None:
                        applicant_number = applicant_info.find('ApplicantNumber').text
                        applicant_name = applicant_info.find('ApplicantName').text
                        corporation_number = applicant_info.find('CorporationNumber').text
                        return applicant_number, applicant_name, corporation_number, None
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

# 메인 실행 부분
def main():
    # 엑셀 파일 로드
    input_file = 'corporation_numbers(100건).xlsx'
    df = pd.read_excel(input_file)

    # biz_no 열을 문자열로 변환
    df['biz_no'] = df['biz_no'].astype(str)

    # 사업자등록번호 처리
    business_registration_numbers = df['biz_no'].dropna().tolist()
    formatted_business_registration_numbers = [
        f"{str(num).strip()[:3]}-{str(num).strip()[3:5]}-{str(num).strip()[5:]}" for num in business_registration_numbers if len(str(num).strip()) == 10
    ]

    # 접근 키
    access_key = os.getenv('SERVICE_KEY')

    # 결과를 저장할 리스트
    applicant_numbers = [None] * len(formatted_business_registration_numbers)
    applicant_names = [None] * len(formatted_business_registration_numbers)
    corporation_numbers = [None] * len(formatted_business_registration_numbers)

    # 시작 시간 기록
    start_time = time.time()

    # 첫 번째 API 호출 (사업자등록번호 기반)
    for index, br_number in enumerate(formatted_business_registration_numbers):
        applicant_number, applicant_name, corporation_number, error_message = get_corp_bs_applicant_info_br(br_number, access_key)
        
        if error_message == "출원인 정보 없음":
            # 두 번째 API 호출 (법인번호 기반)
            if corporation_number:
                formatted_corporation_number = f"{str(int(corporation_number)).strip()[:6]}-{str(int(corporation_number)).strip()[6:]}"
                # 이제 이 formatted_corporation_number를 사용하여 API 호출을 할 수 있습니다.
                applicant_number, applicant_name, corporation_number, error_message = get_corp_bs_applicant_info(
                    formatted_corporation_number, access_key)
            else:
                error_message = "법인번호 없음"

        # 결과 저장
        applicant_numbers[index] = applicant_number
        applicant_names[index] = applicant_name
        corporation_numbers[index] = corporation_number
        print(br_number, applicant_number, applicant_name, corporation_number, error_message)

        time.sleep(1)  # API 요청 간 1초 대기

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

if __name__ == "__main__":
    main()
