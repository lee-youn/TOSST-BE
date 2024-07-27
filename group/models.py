from django.db import models
from user.models import User


class Group(models.Model):
    wake_time = models.TimeField()
    users = models.ManyToManyField(User, blank=True) 
    name = models.CharField(max_length=500)

    class Meta:
        db_table = 'group'