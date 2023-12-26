from .models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            nickname = validated_data['nickname'],
            name = validated_data['name'],
            password = validated_data['password'],
            cover_letter=validated_data.get('cover_letter', None),  # 자기소개서 추가
            occupation=validated_data.get('occupation', None)        # 선호 직업 추가

        )
        return user
    class Meta:
        model = User
        fields = ['nickname', 'email', 'name', 'password','cover_letter', 'occupation']# 필드에 추가