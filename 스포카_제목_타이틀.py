import requests
from bs4 import BeautifulSoup
import json

# JSON 파일 불러오기
with open('result.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

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

# 결과 확인
for result in spoqa_results:
    print(result)
