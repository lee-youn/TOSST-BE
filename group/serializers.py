from rest_framework import serializers
from user.models import User, Wake
from .models import Group


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class GroupRequestSerializer(serializers.ModelSerializer):
    users = UserDataSerializer(many=True, read_only=True)  # Many=True로 설정

    class Meta:
        model = Group
        fields = ['id','name', 'wake_time', 'users']  # 필드 추가

class GroupListSerializer(serializers.Serializer):
    name = serializers.CharField()

class GroupListResponseSerializer(serializers.ModelSerializer):
    users = UserDataSerializer(many=True, read_only=True)
    user_count = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ['id', 'name', 'wake_time', 'users', 'user_count']

    def get_user_count(self, obj):
        return obj.users.count()
    
class UserListRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class UserListResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'profile', 'nickname', 'description']


class WakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wake
        fields = ['status', 'wake_date']