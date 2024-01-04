from celery import shared_task
from .models import Crawling
import csv
import subprocess

@shared_task
def my_scheduled_task():
    # 기존 Crawling 데이터를 모두 삭제합니다.
    Crawling.objects.all().delete()

    # csv 파일을 읽어서 Django의 모델에 데이터를 삽입합니다.
    with open('C:\\Users\\user\\Desktop\\crwaling_merge\\KERNEL\\Crawling\\naver_title_main_img_url_url_1.csv', 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            Crawling.objects.create(
                title=row['title'],
                body=row['body'],
                image=row['image'],
                url=row['url'],
            )
