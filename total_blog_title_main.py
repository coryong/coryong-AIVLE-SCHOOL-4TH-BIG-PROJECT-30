import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import re
import pandas as pd

# JSON 파일 불러오기
with open('result.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 카카오 관련 포스트 URL 추출
kakao_posts = data.get('카카오', [])  # 'kakao' 키로 카카오 관련 포스트 URL 리스트를 가져옵니다.

# 결과를 저장할 리스트
kakao_results = []

for post in kakao_posts:
    url = post['url']
    print(f"처리 중인 URL: {url}")  # 처리 중인 URL 확인
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # 제목 추출
            title = soup.find('h1', class_='elementor-heading-title elementor-size-default')
            if title:
                title_text = title.text.strip()
            else:
                title_text = "제목 없음"

            # 본문 추출
            content_divs = soup.find_all('div', class_='elementor-text-editor elementor-clearfix')
            content_texts = [div.text.strip() for div in content_divs]
            content_text = ' '.join(content_texts)

            kakao_results.append({
                'title': title_text,
                'content': content_text
            })
    except Exception as e:
        print(f"Error while fetching {url}: {e}")
        
        
        
        

# 우아한 형제들 관련 포스트 URL 추출
woowa_posts = data.get('우아한 형제들', [])

# 결과를 저장할 리스트
woowa_results = []

for post in woowa_posts:
    url = post['url']
    print(f"처리 중인 URL: {url}")  # 처리 중인 URL 확인
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # 제목 추출
            title = soup.find('div', class_='post-header').find('h1')
            if title:
                title_text = title.text.strip()
            else:
                title_text = "제목 없음"

            # 본문 추출
            content = soup.find('div', class_='post-content-inner')
            if content:
                content_text = ' '.join(content.stripped_strings)
            else:
                content_text = "내용 없음"

            # 결과 저장
            woowa_results.append({
                'title': title_text,
                'content': content_text
            })
    except Exception as e:
        print(f"Error while fetching {url}: {e}")


# 스포카 관련 포스트 URL 추출
spoqa_posts = data.get('스포카', [])

# 결과를 저장할 리스트
spoqa_results = []

for post in spoqa_posts:
    url = post['url']
    print(f"처리 중인 URL: {url}")  # 처리 중인 URL 확인
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # 제목 추출
            title = soup.find('div', class_='post-author-info').find('h1', class_='post-title')
            if title:
                title_text = title.text.strip()
            else:
                title_text = "제목 없음"

            # 본문 추출
            content = soup.find('div', class_='post')
            if content:
                content_text = ' '.join(content.stripped_strings)
            else:
                content_text = "내용 없음"

            # 결과 저장
            spoqa_results.append({
                'title': title_text,
                'content': content_text
            })
    except Exception as e:
        print(f"Error while fetching {url}: {e}")

    
# SK텔레콤

# 기존에 저장된 SK텔레콤 포스트의 ID를 추출하여 새로운 URL 형식으로 변환하는 함수
def convert_url(old_url):
    post_id = re.search(r'/post/(\d+)', old_url)
    if post_id:
        new_url = f"https://devocean.sk.com/blog/techBoardDetail.do?ID={post_id.group(1)}&boardType=techBlog&searchData=&page=&subIndex="
        return new_url
    return old_url  # 매치되지 않은 경우 원래 URL을 반환

skt_results = []

options = Options()
options.add_argument("--headless")  # 브라우저 창을 띄우지 않는 옵션입니다.
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

for post in data.get('SK텔레콤', []):
    old_url = post['url']
    new_url = convert_url(old_url)
    
    driver.get(new_url)

    try:
        # Explicit Wait 사용
        wait = WebDriverWait(driver, 10)
        title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.sub-view-title > h2')))
        content = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.toastui-editor-contents')))

        title_text = title.text.strip() if title else "제목 없음"
        content_text = content.text.strip() if content else "내용 없음"

        skt_results.append({
            'title': title_text,
            'content': content_text
        })
    except Exception as e:
        print(f"Error while fetching {new_url}: {e}")

driver.quit()

    
# NHN 관련 포스트 URL 추출
nhn_posts = data.get('NHN', [])

# 결과를 저장할 리스트
nhn_results = []
    
# Selenium WebDriver 설정
options = Options()
options.add_argument("--headless")  # 브라우저 창을 띄우지 않는 옵션입니다.
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

for post in nhn_posts:
    url = post['url']
    print(f"처리 중인 URL: {url}")  # 처리 중인 URL 확인
    try:
        driver.get(url)
        time.sleep(2)  # 페이지가 완전히 로드될 때까지 기다립니다.

        # 제목 추출
        title = driver.find_element(By.CSS_SELECTOR, 'h1.detail_tit.ng-binding')
        title_text = title.text.strip() if title else "제목 없음"

        # 본문 추출
        content = driver.find_element(By.CSS_SELECTOR, 'div.tui-editor-contents')
        content_text = content.text.strip() if content else "내용 없음"

        # 결과 저장
        nhn_results.append({
            'title': title_text,
            'content': content_text
        })
    except Exception as e:
        print(f"Error while fetching {url}: {e}")

driver.quit()  # 브라우저 종료

    
# NAVER D2 관련 포스트 URL 추출
naver_d2_posts = data.get('NAVER D2', [])

# 결과를 저장할 리스트
naver_d2_results = []

# Selenium WebDriver 설정
options = Options()
options.add_argument("--headless")  # 브라우저 창을 띄우지 않는 옵션입니다.
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

for post in naver_d2_posts:
    url = post['url']
    print(f"처리 중인 URL: {url}")  # 처리 중인 URL 확인
    try:
        driver.get(url)
        time.sleep(2)  # 페이지가 완전히 로드될 때까지 기다립니다.

        # 제목 추출
        title = driver.find_element(By.CSS_SELECTOR, 'h1.posting_tit')
        title_text = title.text.strip() if title else "제목 없음"

        # 본문 추출
        content = driver.find_element(By.CSS_SELECTOR, 'div.con_view')
        content_text = content.text.strip() if content else "내용 없음"

        # 결과 저장
        naver_d2_results.append({
            'title': title_text,
            'content': content_text
        })
    except Exception as e:
        print(f"Error while fetching {url}: {e}")

driver.quit()  # 브라우저 종료




# 모든 결과 리스트 병합
all_results = kakao_results + woowa_results + spoqa_results + skt_results + nhn_results + naver_d2_results


# 결과를 DataFrame으로 변환
df = pd.DataFrame(all_results, columns=['title', 'content'])

# DataFrame을 CSV 파일로 저장
df.to_csv('results.csv', index=False, encoding='utf-8-sig')

# DataFrame을 JSON 파일로 저장
df.to_json('results_title_main.json', force_ascii=False, orient='records')