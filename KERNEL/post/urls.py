from django.urls import path, include
from .views import PostViewSet, CommentViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# 첫 번째 인자는 url의 prefix
# 두 번째 인자는 ViewSet
router.register('post', PostViewSet, basename='post') # (게시글)
router.register('comment', CommentViewSet, basename='comment') # (댓글)

urlpatterns =[
    path('', include(router.urls))
]