from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import News, NewsKeyword
from .serializers import NewsSerializer, QuizSerializer, WakeSerializer
from quiz.models import Quiz
from user.models import User, Wake
import random

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def news(request):
    if request.method == "GET":
        try:
            news = News.objects.all()
            random_news = random.sample(list(news), min(len(news), 3))
            serializer = NewsSerializer(random_news, many=True)
            return Response({"status": "success", "data": serializer.data})
        except Exception as e:
            return Response({"status": "error", "message": "기사를 가져오지 못했습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def news_quiz(request, id):
    if request.method == "GET":
        try:
            quiz = Quiz.objects.filter(news_id=id).first()
            serializer = QuizSerializer(quiz)
            return Response({"status": "success", "data": serializer.data})
        except Exception as e:
            return Response({"status": "error", "message": "퀴즈를 가져오지 못했습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def quiz_status(request):
    if request.method == "GET":
        user = request.user
        
        try:
            wake = Wake.objects.get(User=user)
        except Wake.DoesNotExist:
            return Response({"status": "error", "message": "Wake 객체를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        # 상태를 2로 업데이트
        wake.status = 2
        wake.save()
        
        # 시리얼라이저를 사용하여 응답 데이터 생성
        serializer = WakeSerializer(wake)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

