from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Crawling, UserCrawlingLike
from .serializers import CrawlingSerializer,UserCrawlingLikeSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from django.http import JsonResponse

# 사용자가 게시물에 "좋아요"를 누를 때 실행되는 함수
def like_crawling(request, user_id, crawling_id):
    # 해당 사용자가 이미 "좋아요"를 눌렀는지 확인
    user_like_crawling = UserCrawlingLike.objects.filter(user_id=user_id, crawling_id=crawling_id)

    if user_like_crawling.exists():  # 이미 "좋아요"를 눌렀다면
        return JsonResponse({'message': 'You already liked this post.'}, status=400)

    # UserLikeCrawling 테이블에 새로운 데이터 추가
    UserCrawlingLike.objects.create(user_id=user_id, crawling_id=crawling_id)

    # 해당 게시물의 "좋아요" 수 계산
    like_count = UserCrawlingLike.objects.filter(crawling_id=crawling_id).count()

    # Crawling 테이블의 like_count 필드 업데이트
    Crawling.objects.filter(id=crawling_id).update(like_count=like_count)

    return JsonResponse({'message': 'Successfully liked the post.'}, status=200)

def get_like_status(crawling_id, user_id):
    return UserCrawlingLike.objects.filter(crawling_id=crawling_id, user_id=user_id).exists()

class CrawlingPostView(viewsets.ModelViewSet):
    queryset = Crawling.objects.all()
    serializer_class = CrawlingSerializer
    permission_classes = [IsAuthenticated]  # 사용자 인증이 필요합니다.

    def perform_create(self, serializer):
        serializer.save()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response = serializer.data
        response['like_status'] = get_like_status(instance.id, request.user.id)  # 좋아요 상태를 반환합니다.
        return Response(response)

        
class CrawlingLikeViewSet(viewsets.ModelViewSet):
    queryset = UserCrawlingLike.objects.all()
    serializer_class = UserCrawlingLikeSerializer

    def create(self, request, *args, **kwargs):
        if UserCrawlingLike.objects.filter(crawling_id=request.data['crawling'], user_id=request.user.id).exists():
            raise ValidationError('You have already liked this post.')
    
        # like_crawling 함수 호출
        like_crawling(request, request.user.id, request.data['crawling'])

        return super().create(request, *args, **kwargs)
    