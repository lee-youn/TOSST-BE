from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import News, NewsKeyword
from .serializers import NewsSerializer, QuizSerializer, WakeSerializer
from quiz.models import Quiz
from user.models import User, Wake
import random

news_key = []

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def news(request):
    if request.method == "GET":
        try:
            news = News.objects.all()
            random_news = random.sample(list(news), min(len(news), 3))
            serializer = NewsSerializer(random_news, many=True)

            global news_key
            news_key = [news_item.id for news_item in random_news]
            print(news_key)

            return Response({"status": "success", "data": serializer.data})
        except Exception as e:
            return Response({"status": "error", "message": "기사를 가져오지 못했습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def news_quiz(request):
    if request.method == "GET":
        try:
            print(news_key)
            # 뉴스 ID들에 맞는 뉴스 데이터 가져오기
            news_items = News.objects.filter(id__in=news_key)
            news_serializer = NewsSerializer(news_items, many=True)

            # 뉴스 ID들에 맞는 퀴즈 데이터 가져오기
            quizzes_data = []
            for news_id in news_key:
                quizzes = Quiz.objects.filter(news_id=news_id).first()
                quiz_serializer = QuizSerializer(quizzes) if quizzes else None
                quizzes_data.append(quiz_serializer.data if quiz_serializer else None)

            return Response({
                "status": "success",
                "news": news_serializer.data,
                "quizzes": quizzes_data
            })
        except Exception as e:
            return Response({"status": "error", "message": "정보를 가져오지 못했습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
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

