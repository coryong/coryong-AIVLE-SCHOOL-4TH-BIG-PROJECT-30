import os
import django
import pandas as pd

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')  # 'myproject'는 실제 Django 프로젝트 이름으로 변경해야 합니다.
django.setup()

from Crawling.models import Crawling  # 'myapp'은 실제 앱 이름으로 변경해야 합니다.

def save_from_csv():
    # Crawling 모델의 모든 인스턴스 삭제
    Crawling.objects.all().delete()
    
    # CSV 파일 읽어오기
    df = pd.read_csv("C:\\Users\\user\\Desktop\\crwaling_merge\\KERNEL\\Crawling\\naver_title_main_img_url_url_1.csv", encoding='utf-8-sig')

    # 각 행에 대해 모델 생성 및 저장
    for idx, row in df.iterrows():
        c = Crawling()
        c.title = row['title']
        c.body = row['body']
        c.image = row['image']
        c.url = row['url']
        c.save()

save_from_csv()
