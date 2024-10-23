import requests
import xml.etree.ElementTree as ET

class CorpAPI:
    def __init__(self, access_key):
        self.access_key = access_key

    def call_api(self, url, params):
        for attempt in range(3):
            try:
                response = requests.get(url, params=params)
                response.raise_for_status()

                root = ET.fromstring(response.content)
                result_code = root.find('.//resultCode').text or '00'
                result_msg = root.find('.//resultMsg').text or "정보 없음"

                if result_code == '00':
                    return root.find('.//corpBsApplicantInfo'), None
                else:
                    return None, f"오류 코드: {result_code}, 메시지: {result_msg}"
            except requests.exceptions.RequestException as e:
                if attempt < 2:
                    time.sleep(3)
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

    def _get_applicant_info(self, url, params):
        applicant_info, error_message = self.call_api(url, params)
        if error_message:
            return None, None, None, error_message
        return self._extract_applicant_info(applicant_info)

    def get_corp_bs_applicant_info_br(self, business_registration_number):
        url = "http://plus.kipris.or.kr/openapi/rest/CorpBsApplicantService/corpBsApplicantInfoV3"
        params = {
            'BusinessRegistrationNumber': business_registration_number,
            'accessKey': self.access_key
        }
        return self._get_applicant_info(url, params)

    def get_corp_bs_applicant_info(self, corporation_number):
        url = "http://plus.kipris.or.kr/openapi/rest/CorpBsApplicantService/corpBsApplicantInfoV2"
        params = {
            'CorporationNumber': corporation_number,
            'accessKey': self.access_key
        }
        return self._get_applicant_info(url, params)
