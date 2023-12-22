import requests
from bs4 import BeautifulSoup
import json
import os
from selenium import webdriver
from urllib.request import urlopen
import ssl
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
import re  # 정규 표현식 모듈을 불러옵니다.
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import UnexpectedAlertPresentException, TimeoutException

# 드라이버 설정
options = Options()
options.headless = True  # 필요한 경우 Headless 모드 활성화
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(3)


dateMatcher = {
    "Jan" : "01",
    "Feb" : "02",
    "Mar" : "03",
    "Apr" : "04",
    "May" : "05",
    "Jun" : "06",
    "Jul" : "07",
    "Aug" : "08",
    "Sep" : "09",
    "Oct" : "10",
    "Nov" : "11",
    "Dec" : "12"
}

# 6 -> 06
# 12 -> 12
# Utility functions
def get_year(date_str):
    # 정규 표현식을 사용하여 연도를 찾습니다.
    match = re.search(r'\b\d{4}\b', date_str)
    if match:
        return int(match.group(0))  # 찾은 연도를 정수로 반환합니다.
    raise ValueError("Valid year not found in date string.")  # 연도를 찾지 못하면 예외를 발생시킵니다.

def day_format(n):
    return str(n).zfill(2)

def extract_post_data(article):
    title_element = article.find_element(By.CSS_SELECTOR, 'h3.title')
    title = title_element.text.strip()
    
    onclick_attr = title_element.get_attribute('onclick')
    post_id = re.search(r"goDetail\(this,'(\d+)',event\)", onclick_attr).group(1)
    link = f"https://devocean.sk.com/blog/post/{post_id}"

    date = article.find_element(By.CSS_SELECTOR, 'span.date').text.strip()

    return {
        "title": title,
        "url": link,
        "date": date
    }
    
data = {}

# 정규 표현식을 사용하여 연도를 찾는 함수
def get_year2(date_str):
    match = re.search(r'(\d{2})\.\d{2}\.\d{2}', date_str)
    if match:
        year = int(match.group(1)) + 2000
        return year
    return None


# SK텔레콤 Devocean 블로그 크롤링
data = {"SK텔레콤": []}
page = 1
is_collecting = True

def close_popup(driver):
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.floating_close'))).click()
        print("Popup closed.")
    except TimeoutException:
        print("No popup was found within the time limit.")
    except Exception as e:
        print(f"An error occurred while closing the popup: {e}")
        
while is_collecting and page <= 27:  # 최대 27 페이지까지 크롤링
    try:
        # 블로그 페이지로 이동
        driver.get(f"https://devocean.sk.com/blog/sub/index.do?ID=&boardType=&searchData=&page={page}&subIndex=%EC%B5%9C%EC%8B%A0+%EA%B8%B0%EC%88%A0+%EB%B8%94%EB%A1%9C%EA%B7%B8")
        
        # 팝업 닫기
        close_popup(driver)
        
        # 게시물이 로드될 때까지 대기
        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.sec-cont')))
        
        # 모든 게시물 정보 추출
        articles = driver.find_elements(By.CSS_SELECTOR, 'div.sec-cont')
        for article in articles:
            post_data = extract_post_data(article)
            data["SK텔레콤"].append(post_data)  # 추출한 데이터를 딕셔너리에 추가

        # 다음 페이지로 이동 준비
        page += 1
        # # 다음 페이지 버튼이 있는지 확인하여 더 이상 수집할 페이지가 없으면 중단
        # next_page_button = driver.find_elements(By.CSS_SELECTOR, 'a.next.page-numbers')
        # if not next_page_button:
        #     is_collecting = False
        
    except TimeoutException:
        print(f"Timed out waiting for page to load on page {page}. Trying to continue...")
    except UnexpectedAlertPresentException:
        alert = Alert(driver)
        alert.accept()
        print("Unexpected alert present.")
    except Exception as e:
        print(f"An error occurred: {e}")

driver.quit()

# 수집된 데이터 출력
print(data)
