from rest_framework import serializers
from .models import News, NewsKeyword
from quiz.models import Quiz
from user.models import Wake

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'url', 'summary', 'published_at']

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id','question', 'answer','comment']

class WakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wake
        fields = ['status', 'wake_date']
