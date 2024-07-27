from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Todo
import requests
from .serializers import TodoSerializer, TodoCreateSerializer, TodoUpdateSerializer, UserSerializer
from datetime import datetime

# 투두리스트 생성
@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def todo_create(request):
    if request.method == 'POST':
        serializer = TodoCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"status": "error", "message": "유효하지 않은 데이터입니다", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        title = serializer.validated_data.get("title")
        
        user = request.user
        
        todo = serializer.save(user_id=user, title = title, todo_date=datetime.now())
        todo_serializer = TodoSerializer(todo)
        return Response(todo_serializer.data, status=status.HTTP_201_CREATED)
    if request.method == 'GET':
        todos = Todo.objects.filter(user_id=request.user)
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# 투두리스트 수정, 삭제
@api_view(['PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def todo_updateDelete(request, id):
    if request.method == 'PATCH':   # 수정
        try:
            user = request.user
            todo = Todo.objects.get(id=id, user_id=request.user.id)
        except Todo.DoesNotExist:
            return Response({"status": "error", "message": "투두 항목을 찾을 수 없습니다"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TodoUpdateSerializer(todo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"status": "error", "message": "유효하지 않은 데이터입니다", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':   # 삭제
        try:
            todo = Todo.objects.get(id=id, user_id=request.user)
        except Todo.DoesNotExist:
            return Response({"status": "error", "message": "투두 항목을 찾을 수 없습니다"}, status=status.HTTP_404_NOT_FOUND)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

