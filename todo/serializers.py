from rest_framework import serializers
from .models import Todo
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

# 투두 직렬화기
class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'

# 투두 항목 생성 시
class TodoCreateSerializer(serializers.ModelSerializer):
    title = serializers.CharField()

    class Meta:
        model = Todo
        fields = ['title']

# 투두 항목 수정 시
class TodoUpdateSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = Todo
        fields = ['user_id','title','status']