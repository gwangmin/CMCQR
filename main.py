'''
Get CMC QR script
using headless chrome, selenium

selenium chrome:
https://greeksharifa.github.io/references/2020/10/30/python-selenium-usage/
'''

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
import time
import requests
from bs4 import BeautifulSoup
import base64

def get_qr():
    '''
    Get CMC QR data
    using headless chrome, selenium

    return: number code(qr content), qr img tag source code, base64 encoded qr
    '''
    # virtual display for screenless server
    # https://somjang.tistory.com/entry/Ubuntu-Ubuntu-%EC%84%9C%EB%B2%84%EC%97%90-Selenium-%EC%84%A4%EC%B9%98%ED%95%98%EA%B3%A0-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0
    #from pyvirtualdisplay import Display
    #display = Display(visible=0, size=(1920, 1080))
    #display.start()

    # chrome options
    options = webdriver.ChromeOptions()
    # options.add_argument('window-size=1920x1080')
    # options.add_argument('disable-gpu')
    # options.add_argument('start-maximized')
    # options.add_argument('disable-infobars')
    # options.add_argument('--disable-extensions')
    # options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # options.add_experimental_option('useAutomationExtension', False)
    # options.add_argument('--disable-blink-features=AutomationControlled')
    # options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
    # in docker
    options.add_argument('headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # load chrome
    path = chromedriver_autoinstaller.install()
    driver = webdriver.Chrome(path, options=options)

    driver.implicitly_wait(5)

    # url
    URL = 'https://kiosk.cmcseoul.or.kr/step_patient.php'
    driver.get(URL)

    # form 입력
    #################### 개인정보 입력 ####################
    data = {
        '주민등록번호 앞자리' : '000000', '주민등록번호 뒷자리' : '0000000',
        '이름' : '홍길동',
        '전화번호1' : '010', '전화번호2' : '0000', '전화번호3' : '0000',
        '질문1' : 1,
        '질문2' : 1,
        '질문3' : 1
    }

    driver.find_element_by_css_selector('#user_no1').send_keys(data['주민등록번호 앞자리'])
    driver.find_element_by_css_selector('#user_no2').send_keys(data['주민등록번호 뒷자리'])
    driver.find_element_by_css_selector('#user_name').send_keys(data['이름'])
    driver.find_element_by_css_selector('#user_selphone2').send_keys(data['전화번호2'])
    driver.find_element_by_css_selector('#user_selphone3').send_keys(data['전화번호3'])
    chkA = driver.find_element_by_css_selector('#chkA' + str(data['질문1']))
    chkB = driver.find_element_by_css_selector('#chkB' + str(data['질문2']))
    chkC = driver.find_element_by_css_selector('#chkC' + str(data['질문3']))
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
    img_tag = page.select('#qrimg_btn > center > div.qr > img')[0]
    tmp = img_tag['src']
    qr_b64 = tmp[tmp.find(',')+1:]

    driver.quit()
    return code, str(img_tag), qr_b64


def write_qr_png(qr_b64, path):
    '''
    Write base64 encoded qr in png file

    qr_b64: base64 encoded qr img
    path: saved png file path
    '''
    with open(path, 'wb') as f:
        f.write(base64.b64decode(qr_b64))
