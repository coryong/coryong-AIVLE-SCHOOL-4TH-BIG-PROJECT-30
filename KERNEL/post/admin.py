from django.contrib import admin

# Register your models here.
from .models import Post
# Register your models here.
# TechnologyStack 모델을 관리자 사이트에 등록합니다.
admin.site.register(Post)