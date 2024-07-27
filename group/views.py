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
from .serializers import  UserDataSerializer, GroupRequestSerializer, GroupListSerializer, GroupListResponseSerializer, UserListRequestSerializer, UserListResponseSerializer
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.shortcuts import render, get_object_or_404
from .models import Group
from user.models import User, Wake

@api_view(["POST","GET", "DELETE"])
@permission_classes([IsAuthenticated])
def group(request):
    if request.method == "POST":
        group_serializer = GroupRequestSerializer(data=request.data)
        if not group_serializer.is_valid():
            return Response(group_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        group_data = group_serializer.validated_data
        group_name = group_data.get('name')
        wake_time = group_data.get('wake_time')
        users_ids = group_data.get('users', [])  # 기본값으로 빈 리스트 사용

        # 그룹이 존재하지 않으면 생성
        group = Group.objects.create(
            name=group_name,
            wake_time=wake_time
        )
        
        request.user.wake_date = wake_time
        request.user.save()

        # 사용자 목록을 가져와서 그룹에 추가
        users_list = User.objects.filter(id__in=users_ids)
        if request.user not in users_list:
            users_list = list(users_list) + [request.user]  # 현재 사용자를 추가
        else:
            users_list = list(users_list)
        
        # 그룹에 사용자 추가
        group.users.set(users_list)
        group.save()
        
        # 그룹을 시리얼라이즈해서 응답
        response_serializer = GroupRequestSerializer(group)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    

    

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_group(request):
    if request.method == "GET":
        user = request.user
        groups = Group.objects.filter(users = user )
        # 그룹을 시리얼라이즈해서 응답
        serializer = GroupListResponseSerializer(groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["DELETE", "PATCH", "POST"])
@permission_classes([IsAuthenticated])
def group_data(request, id):
    if request.method == "DELETE":
        group = Group.objects.get(id=id)
        group.delete()
        return Response(status=status.HTTP_200_OK)
    if request.method == "PATCH":
        try:
            group = Group.objects.get(id=id)
        except Group.DoesNotExist:
            return Response({'detail': '해당 그룹을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = GroupRequestSerializer(group, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        group = serializer.save()
        group_serializer= GroupListResponseSerializer(group)
        return Response(group_serializer.data, status=status.HTTP_200_OK)
    if request.method == "POST":
        email_serializer = UserListRequestSerializer(data = request.data)
        if not email_serializer.is_valid():
            return Response(email_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        email = email_serializer.validated_data["email"]
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # 그룹 조회
        try:
            group = Group.objects.get(id=id)
        except Group.DoesNotExist:
            return Response({'detail': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)

        # 그룹에 사용자 추가
        group.users.add(user)  # 단일 사용자 추가 시 `add` 사용
        group.save()

        wake, created = Wake.objects.get_or_create(User=user)
        wake.wake_date = group.wake_time  # 그룹의 시간으로 업데이트
        wake.save()

        # 그룹 데이터 반환
        response_serializer = GroupRequestSerializer(group)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


        

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def group_user_list(request):
    if request.method == "POST":
        email_serializer = UserListRequestSerializer(data = request.data)
        if not email_serializer.is_valid():
            return Response(email_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        email = email_serializer.validated_data["email"]

        user = User.objects.get(email = email)
        user_serializer = UserListResponseSerializer(user)
        return Response(user_serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def group_list(request):
    if request.method == "POST":
        group_serializer = GroupListSerializer(data=request.data)
        if not group_serializer.is_valid():
            return Response(group_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        group_name = group_serializer.validated_data.get("name")
        try:
            groups = Group.objects.filter(name=group_name)
        except Group.DoesNotExist:
            return Response({'error': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)
        
        response_serializer = GroupListResponseSerializer(groups, many=True)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def group_user_status(request):
    if request.method == "GET":
        user = request.user
        groups = Group.objects.filter(users=user)
        
        user_groups = []
        
        for group in groups:
            # 그룹에 속한 모든 사용자에 대해 Wake 정보를 가져옴
            user_wakes = Wake.objects.filter(User__in=group.users.all())
            wake_data = {}
            
            for wake in user_wakes:
                user_id = wake.User.id
                if user_id not in wake_data:
                    wake_data[user_id] = []
                wake_data[user_id].append({
                    'status': wake.status,
                    'wake_date': wake.wake_date
                })
            
            user_groups.append({
                'group_id': group.id,
                'group_name': group.name,
                'users': [
                    {
                        'id': user.id,
                        'email': user.email,
                        'nickname': user.nickname,
                        "description": user.description,
                        "profile": user.profile.url if user.profile else None,  # 프로필 이미지 URL 처리
                        'wakes': wake_data.get(user.id, [])  # 각 사용자에 대한 Wake 정보
                    }
                    for user in group.users.all()
                ]
            })
            return Response(user_groups, status=status.HTTP_200_OK)


