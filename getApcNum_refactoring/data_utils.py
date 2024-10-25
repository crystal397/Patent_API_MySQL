import pandas as pd
import aiohttp
import asyncio

def load_data(input_file):
    df = pd.read_excel(input_file)
    df['biz_no'] = df['biz_no'].astype(str)
    return df

def format_business_registration_numbers(df):
    return [
        f"{str(num).strip()[:3]}-{str(num).strip()[3:5]}-{str(num).strip()[5:]}"
        for num in df['biz_no'].dropna().tolist() if len(str(num).strip()) == 10
    ]

def save_results(df, output_file):
    df.to_excel(output_file, index=False)

async def process_applicant_info(api_client, formatted_business_registration_numbers):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for br_number in formatted_business_registration_numbers:
            tasks.append(handle_br_number(api_client, session, br_number))
        return await asyncio.gather(*tasks)

async def handle_br_number(api_client, session, br_number):
    applicant_number, applicant_name, corporation_number, error_message = await api_client.get_corp_bs_applicant_info_br(session, br_number)

    if error_message == "출원인 정보 없음" and corporation_number:
        formatted_corporation_number = f"{str(int(corporation_number)).strip()[:6]}-{str(int(corporation_number)).strip()[6:]}"
        applicant_number, applicant_name, corporation_number, error_message = await api_client.get_corp_bs_applicant_info(session, formatted_corporation_number)

    return br_number, applicant_number, applicant_name, corporation_number, error_message