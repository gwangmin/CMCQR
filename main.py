'''
crawling using
chrome selenium
'''

import chromedriver_autoinstaller
from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
import time
import requests
from bs4 import BeautifulSoup
import base64

# virtual display for screenless server
display = Display(visible=0, size=(1920, 1080))
display.start()

# chrome options
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
# options.add_argument('window-size=1920x1080')
# options.add_argument('disable-gpu')
# options.add_argument('start-maximized')
# options.add_argument('disable-infobars')
# options.add_argument('--disable-extensions')
# options.add_experimental_option('excludeSwitches', ['enable-automation'])
# options.add_experimental_option('useAutomationExtension', False)
# options.add_argument('--disable-blink-features=AutomationControlled')
# options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')

# load chrome
path = chromedriver_autoinstaller.install()
driver = webdriver.Chrome(path, options=options)

driver.implicitly_wait(5)

# url
URL = 'https://kiosk.cmcseoul.or.kr/step_patient.php'
driver.get(URL)

# form 입력
# 개인정보...
driver.find_element_by_css_selector('#user_no1').send_keys('')
driver.find_element_by_css_selector('#user_no2').send_keys('')
driver.find_element_by_css_selector('#user_name').send_keys('')
driver.find_element_by_css_selector('#user_selphone2').send_keys('')
driver.find_element_by_css_selector('#user_selphone3').send_keys('')
chkA = driver.find_element_by_css_selector('#chkA1')
chkB = driver.find_element_by_css_selector('#chkB2')
chkC = driver.find_element_by_css_selector('#chkC2')
driver.execute_script("arguments[0].click();", chkA)
driver.execute_script("arguments[0].click();", chkB)
driver.execute_script("arguments[0].click();", chkC)
# 확인
driver.find_element_by_css_selector('#form > div.btn_wrap > input').click()
driver.find_element_by_css_selector('#agree_frame > div > div.btn_wrap > input.btn_mini').click()
# result page
page = BeautifulSoup(driver.page_source, 'html.parser')
# 숫자 코드 -> qr img
code = page.select('#qrimg_btn > center > div.qr')[0]['title']
# 한 번 디코딩 하면 qr.png 바이너리가 나옴
tmp = page.select('#qrimg_btn > center > div.qr > img')[0]['src']
qr_b64 = tmp[tmp.find(',')+1:]

def write_qr_png(qr_b64, path):
    '''
    Write base64 encoded qr in png file

    qr_b64: base64 encoded qr img
    path: saved png file path
    '''
    with open(path, 'wb') as f:
        f.write(base64.b64decode(qr_b64))

#driver.quit()
