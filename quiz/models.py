from django.db import models
from news.models import News

class Quiz(models.Model):
    question = models.CharField(max_length=1000)
    answer = models.BooleanField()
    comment = models.CharField(max_length=1000)
    news = models.ForeignKey(News, on_delete=models.CASCADE)

    class Meta:
        db_table = "quiz"
