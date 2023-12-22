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


# 야놀자
arr = []
for i in range(1, 3):
    if(i == 1):
        res = requests.get('https://yanolja.github.io/')
        html = res.content
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    else:
        res = requests.get("https://yanolja.github.io/page"+str(i))
        html = res.content
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')

    urls = soup.select('#content > article > header > h2 > a')
    atag = soup.select('#content > article > header > h2 > a')
    date = soup.select('#content > article > footer > time')

    n = 1
    for url in urls:
        # 날짜 만들기
        dateText = date[n-1].text
        year = dateText[7:11]

        # 2023년 데이터만 처리
        if year != "2023":
            continue

        month = dateMatcher[dateText[3:6]]
        day = dateText[0:2]
        resDate = year + "." + month + "." + day

        arr.append({"title" : url.text, "url" : "https://yanolja.github.io" + atag[n-1].get('href'), "date" : resDate})
        print(url.text +" "+ "https://yanolja.github.io" + atag[n-1].get('href') + " " + resDate)
        n += 1  
 
driver.quit()
   
data["야놀자"] = arr

# 수집된 데이터 출력
print(data)
