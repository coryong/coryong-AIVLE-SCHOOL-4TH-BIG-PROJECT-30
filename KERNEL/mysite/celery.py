from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Django의 settings 모듈을 Celery의 기본 설정으로 사용하도록 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

app = Celery('mysite', broker='redis://localhost:6379/0')

# Django의 설정을 사용하도록 Celery 애플리케이션을 설정
app.config_from_object('django.conf:settings', namespace='CELERY')

# 모든 Django 앱을 자동으로 찾아 작업을 로드합니다.
app.autodiscover_tasks()