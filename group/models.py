from django.db import models
from user.models import User


class Group(models.Model):
    wake_time = models.TimeField()
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)

    class Meta:
        db_table = 'group'
