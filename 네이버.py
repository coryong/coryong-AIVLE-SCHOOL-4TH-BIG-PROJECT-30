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


# NAVER D2 데이터 수집
arr = []
page = 0
is_collecting = True

while is_collecting:
    driver.get(f'https://d2.naver.com/home?page={page}')

    for i in range(1, 21):
        try:
            title_xpath = f'//*[@id="container"]/div/div/div[{i}]/div/h2/a'
            date_xpath = f'//*[@id="container"]/div/div/div[{i}]/div/dl/dd[1]'

            title = driver.find_element(By.XPATH, title_xpath).text
            atag = driver.find_element(By.XPATH, title_xpath).get_attribute('href')
            date = driver.find_element(By.XPATH, date_xpath).text
            
            # 2023년 이전의 글은 수집하지 않음
            if '2023' not in date:
                is_collecting = False
                break

            arr.append({"title": title, "url": atag, "date": date})
            print(title + " " + atag + " " + date)

        except Exception as e:
            print(f"Error occurred at iteration {i}: {e}")
            break

    # 다음 페이지로 이동
    if is_collecting:
        page += 1
        time.sleep(1)  # 페이지 로딩 대기

driver.quit()

# 수집된 데이터 저장
data["NAVER D2"] = arr

# 수집된 데이터 출력
print(data)
