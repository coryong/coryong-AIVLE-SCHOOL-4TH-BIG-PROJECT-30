from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json
import re

options = Options()
options.headless = True
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

with open('result.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 기존에 저장된 SK텔레콤 포스트의 ID를 추출하여 새로운 URL 형식으로 변환하는 함수
def convert_url(old_url):
    post_id = re.search(r'/post/(\d+)', old_url)
    if post_id:
        new_url = f"https://devocean.sk.com/blog/techBoardDetail.do?ID={post_id.group(1)}&boardType=techBlog&searchData=&page=&subIndex="
        return new_url
    return old_url  # 매치되지 않은 경우 원래 URL을 반환

skt_results = []

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

# 결과 출력
for result in skt_results:
    print(result)
