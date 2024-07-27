from rest_framework import serializers
from user.models import User


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

# class RegisterRequestSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField()

# class RegisterResponseSerializer(serializers.ModelSerializer):
#     user_id = serializers.CharField()
#     class Meta:
#         model = User
#         fields = ['user_id', 'email', 'password']

# class UserLoginRequestSerializer(serializers.Serializer):
#     user_id = serializers.CharField()
