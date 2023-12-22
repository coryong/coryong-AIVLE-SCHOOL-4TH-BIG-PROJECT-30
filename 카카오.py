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


# 우아한 형제들
data = {"우아한 형제들": []}
page = 1
is_collecting = True

while is_collecting:
    try:
        # Navigate to the blog page
        driver.get(f"https://techblog.woowahan.com/?paged={page}")

        # Wait for the articles to be loaded on the page
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.post-item'))
        )
        
        # Get all articles
        articles = driver.find_elements(By.CSS_SELECTOR, '.post-item')
        
        for article in articles:
            title_element = article.find_element(By.CSS_SELECTOR, 'h2.post-title')
            title = title_element.text.strip()
            link_element = article.find_element(By.XPATH, ".//a[.//h2[@class='post-title']]")
            link = link_element.get_attribute('href')
            
            try:
                date_element = article.find_element(By.CSS_SELECTOR, 'time.post-author-date')
                date = date_element.text.strip()
                post_year = get_year(date)
            except ValueError:
                # 날짜 정보가 없거나 형식이 잘못되었을 경우를 처리합니다.
                print(f"날짜 정보가 없거나 잘못되었습니다: {title}")
                continue  # 다음 게시물로 계속합니다.
            
            if post_year == 2023:
                data["우아한 형제들"].append({"title": title, "url": link, "date": date})
            elif post_year < 2023:
                is_collecting = False
                break

        # Check if there is a next page
        next_page = driver.find_elements(By.CSS_SELECTOR, 'a.page.larger')
        if not next_page:
            is_collecting = False
        else:
            page += 1

    except TimeoutException:
        print(f"Timed out waiting for page to load on page {page}")
        break
    except Exception as e:
        print(f"An error occurred on page {page}: {e}")
        break

driver.quit()

# 수집된 데이터 출력
print(data)
