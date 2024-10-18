# Patent_API_MySQL

### 활용 사이트, REST API
https://plus.kipris.or.kr/

### 중요 데이터(Key 값 등) github에 노출하지 않는 방법
1. .env 파일 생성 후, Key 값(```SERVICE_KEY = ''```)을 입력합니다.
2. .gitignore 파일 생성 후, .env를 입력합니다.
3. 만드는 파이썬 코드에서는 아래와 같이 활용하면 됩니다.
```
import os
from dotenv import load_dotenv

load_dotenv()

SERVICE_KEY = os.getenv('SERVICE_KEY')
```

### 0. TEST
**API.py**
1. API 엔드포인트 URL에 요청 파라미터를 설정하여 GET 요청을 보냅니다.
2. XML 데이터 파싱을 하고 필요한 정보 추출 및 출력, 이미지 다운로드를 한 뒤, 총 개수를 출력합니다.

**API_MySQL.py**
0. 미리 MySQL에 데이터베이스, 테이블을 만듭니다.
1. (이미지 다운로드는 하지 않고) API.py에서 얻은 정보를 MySQL로 전송합니다.

**API_MySQL_time.py**
1. API_MySQL.py에 정보의 갯수를 30개에서 50개로 늘리되, 1초마다 다음 페이지의 정보까지 모든 정보를 모두 출력합니다.

  
### 1. '사업자등록번호'를 통해 '특허고객번호'를 가져오기
**getApxNum.py**

### 2. '특허고객번호'로 '등록상태' 등 정보 가져오기
