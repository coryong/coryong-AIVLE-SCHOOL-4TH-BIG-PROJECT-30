from django.contrib import admin
from .models import TechnologyStack, Occupation
# Register your models here.
# TechnologyStack 모델을 관리자 사이트에 등록합니다.
admin.site.register(TechnologyStack)
admin.site.register(Occupation)