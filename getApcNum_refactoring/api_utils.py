import aiohttp
from lxml import etree  # lxml을 임포트

class CorpAPI:
    def __init__(self, access_key):
        self.access_key = access_key

    async def call_api(self, session, url, params):
        for attempt in range(3):
            try:
                async with session.get(url, params=params) as response:
                    response.raise_for_status()
                    xml_content = await response.text()
                    root = etree.fromstring(xml_content.encode('utf-8'))
                    result_code = root.find('.//resultCode').text or '00'
                    result_msg = root.find('.//resultMsg').text or "정보 없음"

                    if result_code == '00':
                        return root.find('.//corpBsApplicantInfo'), None
                    else:
                        return None, f"오류 코드: {result_code}, 메시지: {result_msg}"
            except aiohttp.ClientError as e:
                if attempt < 2:
                    await asyncio.sleep(3)
                else:
                    return None, f"요청 오류: {e}"

    def _extract_applicant_info(self, applicant_info):
        if applicant_info is not None:
            return (
                applicant_info.find('ApplicantNumber').text,
                applicant_info.find('ApplicantName').text,
                applicant_info.find('CorporationNumber').text,
                None
            )
        return None, None, None, "출원인 정보 없음"

    async def _get_applicant_info(self, session, url, params):
        applicant_info, error_message = await self.call_api(session, url, params)
        if error_message:
            return None, None, None, error_message
        return self._extract_applicant_info(applicant_info)

    async def get_corp_bs_applicant_info_br(self, session, business_registration_number):
        url = "http://plus.kipris.or.kr/openapi/rest/CorpBsApplicantService/corpBsApplicantInfoV3"
        params = {
            'BusinessRegistrationNumber': business_registration_number,
            'accessKey': self.access_key
        }
        return await self._get_applicant_info(session, url, params)

    async def get_corp_bs_applicant_info(self, session, corporation_number):
        url = "http://plus.kipris.or.kr/openapi/rest/CorpBsApplicantService/corpBsApplicantInfoV2"
        params = {
            'CorporationNumber': corporation_number,
            'accessKey': self.access_key
        }
        return await self._get_applicant_info(session, url, params)api_
