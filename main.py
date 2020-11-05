import requests
from bs4 import BeautifulSoup

# requests
url = 'https://kiosk.cmcseoul.or.kr/result.php'
data = {
    'user_no1' : '123456', 'user_no2' : '1111111',
    'user_name' : '홍길동',
    'user_selphone1' : '010', 'user_selphone2' : '1234', 'user_selphone3' : '5678',
    'chkA' : 1,
    'chkB' : 'N',
    'chkC' : 'N'
}
resp = requests.post(url, data, verify=False)

# parsing
soup = BeautifulSoup(resp.text, 'html.parser')
last_script = str(soup.select('script')[-1])
start_idx = last_script.find('text: ') + 7
code = last_script[start_idx:].split('\'')[0]

# create QR code
# creat_QR(code)
# https://www.the-qrcode-generator.com/
