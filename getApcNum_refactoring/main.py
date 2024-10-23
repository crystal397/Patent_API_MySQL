import time
from api_utils import CorpAPI
from data_utils import load_data, format_business_registration_numbers, save_results, process_applicant_info
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    input_file = 'corporation_numbers(100건).xlsx'
    output_file = 'business_registration_results.xlsx'
    access_key = os.getenv('SERVICE_KEY')

    df = load_data(input_file)
    formatted_business_registration_numbers = format_business_registration_numbers(df)

    api_client = CorpAPI(access_key)

    start_time = time.time()
    results = process_applicant_info(api_client, formatted_business_registration_numbers)
    execution_time = time.time() - start_time

    # 결과를 데이터프레임에 추가
    df['ApplicantNumber'] = [result[1] for result in results]
    df['ApplicantName'] = [result[2] for result in results]
    df['CorporationNumber'] = [result[3] for result in results]

    save_results(df, output_file)

    print(f"결과가 {output_file}에 저장되었습니다.")
    print(f"총 소요 시간: {execution_time:.2f}초")


if __name__ == "__main__":
    main()