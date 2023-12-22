from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import json

# Selenium WebDriver 설정
options = Options()
options.add_argument("--headless")  # 브라우저 창을 띄우지 않는 옵션입니다.
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# JSON 파일 불러오기
with open('result.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# NHN 관련 포스트 URL 추출
nhn_posts = data.get('NHN', [])

# 결과를 저장할 리스트
nhn_results = []

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

# 결과 확인
for result in nhn_results:
    print(result)
