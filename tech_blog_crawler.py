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

# 카카오 블로그 데이터 수집
arr = []
page = 1
is_collecting = True
crawled_urls = set()  # 이미 크롤링한 URL을 추적하기 위한 집합

while is_collecting:
    driver.get(f'https://tech.kakao.com/blog/page/{page}/#posts')

    # 페이지가 로드될 때까지 기다리기
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'elementor-post'))
    )
    
    articles = driver.find_elements(By.CLASS_NAME, 'elementor-post')
    for article in articles:
        try:
            title_element = article.find_element(By.CLASS_NAME, 'elementor-post__title')
            title = title_element.text.strip()
            link = title_element.find_element(By.TAG_NAME, 'a').get_attribute('href')
            date = article.find_element(By.CLASS_NAME, 'elementor-post-date').text.strip()

            # 중복된 게시물은 크롤링하지 않음
            if link in crawled_urls:
                continue

            # 2023년 데이터만 수집
            if '2023' in date:
                arr.append({"title": title, "url": link, "date": date})
                print(title + " " + link + " " + date)
                crawled_urls.add(link)  # URL을 크롤링한 집합에 추가
            else:
                # 2023년 이전 게시물을 만나면 현재 페이지의 크롤링을 종료
                is_collecting = False
                break

        except Exception as e:
            print(f"Error occurred during scraping: {e}")
            # Optionally, you could choose to continue rather than breaking the loop if an error occurs for a single post
            # continue 

    # 다음 페이지 버튼의 존재 여부를 체크하고 없으면 크롤링 종료
    try:
        next_button = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a.next.page-numbers'))
        )
        if next_button:
            page += 1
            time.sleep(1)  # 페이지 로딩 대기
        else:
            is_collecting = False
    except TimeoutException:
        # 다음 페이지 버튼이 없다면, 더 이상 크롤링할 페이지가 없다고 간주하고 크롤링을 종료
        is_collecting = False
    
driver.quit()

# 수집된 데이터 저장
data["카카오"] = arr
    

# 우아한 형제들
# 드라이버 설정
options = Options()
options.headless = True  # 필요한 경우 Headless 모드 활성화
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(3)

data["우아한 형제들"] = []
page = 1
is_collecting = True

while is_collecting:
    try:
        # Navigate to the blog page
        driver.get(f"https://techblog.woowahan.com/?paged={page}")

        # Wait for the articles to be loaded on the page
        WebDriverWait(driver, 10).until(
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

# 스포카
# 드라이버 설정
options = Options()
options.headless = True  # 필요한 경우 Headless 모드 활성화
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(3)
 
arr = []
for i in range(1, 12):
    if(i == 1):
        context = ssl._create_unverified_context()
        res = urlopen("https://spoqa.github.io", context=context)
        soup = BeautifulSoup(res.read(), 'html.parser', from_encoding='utf-8')
    else:
        context = ssl._create_unverified_context()
        res = urlopen("https://spoqa.github.io/page"+str(i), context=context)
        soup = BeautifulSoup(res.read(), 'html.parser', from_encoding='utf-8')

    urls = soup.select('body > div > div.content > div.posts > ul > li > div > h2 > a > span')
    atag = soup.select('body > div > div.content > div.posts > ul > li > div > h2 > a')
    date = soup.select('body > div > div.content > div.posts > ul > li > div > span.post-date')

    n = 1

    for url in urls:
        # 날짜 가져오기
        dateText = date[n-1].text
        year = dateText[0:4]
        
        # 2023년 데이터만 처리
        if year != "2023":
            continue

        month = dateText[6:8]
        day = dateText[10:12]
        resDate = year + "." + month + "." + day

        #a 다듬기 ..   . 이 앞에 붙어있다
        resHref = atag[n-1].get('href')[atag[n-1].get('href').find("/"):len(atag[n-1].get('href'))]
        arr.append({"title" : url.text, "url" : "https://spoqa.github.io" + resHref, "date" : resDate})
        print(url.text +" "+ "https://spoqa.github.io" + resHref + " " + resDate)
        n += 1  

driver.quit()
    
data["스포카"] = arr
 
# SK텔레콤 Devocean
# SK텔레콤 Devocean 블로그 크롤링
# 드라이버 설정
options = Options()
options.headless = True  # 필요한 경우 Headless 모드 활성화
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(3)

# SK텔레콤 Devocean 블로그 크롤링
data["SK텔레콤"] = []
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


# NHN (최신)
# 드라이버 설정
options = Options()
options.headless = True  # 필요한 경우 Headless 모드 활성화
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(3)

arr = []

for i in range(1, 2):  # 원하는 페이지 수에 따라 범위를 조절
    driver.get(f'https://meetup.toast.com/?page={i}')

    for j in range(1, 13):
        title = driver.find_element(By.XPATH, f'//*[@id="content"]/div/div[2]/ul/li[{j}]/a/div/h3').text
        atag = driver.find_element(By.XPATH, f'//*[@id="content"]/div/div[2]/ul/li[{j}]/a').get_attribute('href')
        date = driver.find_element(By.XPATH, f'//*[@id="content"]/div/div[2]/ul/li[{j}]/a/div/div[2]/span[1]').text
        date = date[4:len(date)]
        arr.append({"title": title, "url": atag, "date": date})
        print(title + " " + atag + " " + date)

driver.quit() # 필요에 따라 driver를 종료할 수 있습니다. 다른 작업에서도 WebDriver가 필요하다면 이 코드를 주석 처리하거나 제거합니다.

data["NHN"] = arr


# NAVER D2 데이터 수집
# 드라이버 설정
options = Options()
options.headless = True  # 필요한 경우 Headless 모드 활성화
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(3)

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


# # 모든 내용 json 파일화
# file = open('result.json','w', -1, "utf-8")
# json.dump(data, file, ensure_ascii=False)
# file.close

# 모든 내용 json 파일화
file = open('result.json','w', -1, "utf-8")
json.dump(data, file, ensure_ascii=False)
file.close()
