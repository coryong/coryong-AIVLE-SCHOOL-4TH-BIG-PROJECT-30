import requests
from bs4 import BeautifulSoup
import json

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

# 결과 확인
for result in kakao_results:
    print(result)
