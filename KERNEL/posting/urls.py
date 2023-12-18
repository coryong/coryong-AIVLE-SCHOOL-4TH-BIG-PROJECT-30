from django.urls import path
from .views import show
app_name = 'posting'
urlpatterns = [
    path('', show, name='posting'),
]