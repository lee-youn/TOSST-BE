from django.db import models
from user.models import User


class News(models.Model):
    title = models.CharField(max_length=500)
    url = models.URLField()
    summary = models.TextField()
    published_at = models.DateField()

    class Meta:
        db_table = 'news'

class NewsKeyword(models.Model):
    keyword = models.CharField(max_length=128)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    News = models.ForeignKey(News, on_delete=models.CASCADE)

    class Meta:
        db_table = "news_keyword"
