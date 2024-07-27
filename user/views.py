from django.shortcuts import render
import os

import requests
import jwt

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.serializers import Serializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, UserDataSerializer, WakeSerializer
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.shortcuts import render, get_object_or_404
from .models import User,Wake
from django.utils import timezone
from django.utils.timezone import localtime
from datetime import timedelta



@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        # Wake 객체 생성
        wake = Wake.objects.create(User=user)
        wake.save()
            
        # jwt 토큰 접근
        token = TokenObtainPairSerializer.get_token(user)
        refresh_token = str(token)
        access_token = str(token.access_token)
        res = Response(
            {
                "user": serializer.data,
                "message": "register successs",
                "token": {
                    "access": access_token,
                    "refresh": refresh_token,
                },
            },
            status=status.HTTP_200_OK,
        )
        
        # jwt 토큰 => 쿠키에 저장
        res.set_cookie("access", access_token, httponly=True)
        res.set_cookie("refresh", refresh_token, httponly=True)
            
        return res
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    user = authenticate(
            email=request.data.get("email"), password=request.data.get("password")
        )
        # 이미 회원가입 된 유저일 때
    if user is not None:
        serializer = UserSerializer(user)
        # jwt 토큰 접근
        token = TokenObtainPairSerializer.get_token(user)
        refresh_token = str(token)
        access_token = str(token.access_token)
        res = Response(
            {
                "user": serializer.data,
                "message": "login success",
                "token": {
                    "access": access_token,
                    "refresh": refresh_token,
                },
            },
                status=status.HTTP_200_OK,
            )
        try:
            wake = Wake.objects.get(User=user)
            wake.status = 1
            wake.save()
            
        except Wake.DoesNotExist:
            # Wake 객체가 없는 경우 새로 생성
            Wake.objects.create(User=user)
            # jwt 토큰 => 쿠키에 저장
        res.set_cookie("access", access_token, httponly=True)
        res.set_cookie("refresh", refresh_token, httponly=True)
        return res
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["PATCH", "GET"])
@permission_classes([IsAuthenticated])
def user(request):
    if request.method == "PATCH":
        serializer = UserDataSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            if 'profile' in request.FILES:
                serializer.validated_data['profile'] = request.FILES['profile']
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "GET":
        user = get_object_or_404(User, email=request.user.email)
        serializer = UserDataSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_wake(request):
    if request.method == "GET":
        user = request.user  # request.user는 이미 User 인스턴스입니다.
        wakes = Wake.objects.get(User=user)

        future_wake_date = wakes.wake_date + timedelta(minutes=30)
        timenow = timezone.now()
        if future_wake_date >= timenow:
            wakes.status = 1
        else:
            wakes.status = 3
        
        wakes.save()

        # 시리얼라이저를 사용하여 응답
        serializer = WakeSerializer(wakes)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def wake_status_monthly(request):
    month = request.query_params.get('month')

    print(month)
    # 잘못된 입력 검사
    try:
        month = int(month)
        if month < 1 or month > 12:
            raise ValueError
    except ValueError:
        return Response({"status": "error", "message": "1 ~ 12월 중 선택해주세요"}, status=status.HTTP_400_BAD_REQUEST)

    # 인증된 사용자 정보 가져오기
    user = request.user

    # 'Wake' 모델에서 'month'와 'user'로 필터링
    # 'User' 필드 또는 'User_id' 필드를 사용해야 함
    wakes = Wake.objects.filter(User=user, wake_date__month=month).order_by('wake_date')

    # 데이터 직렬화
    serializer = WakeSerializer(wakes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



