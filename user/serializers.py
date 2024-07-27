from rest_framework import serializers
from user.models import User, Wake


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            password = validated_data['password']
        )
        return user

class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class WakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wake
        fields = ['status', 'wake_date']  # 필요한 필드만 포함시킬 수 있습니다.