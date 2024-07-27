from django.db import models
from user.models import User

class Todo(models.Model):
    todo_date = models.DateField()
    status = models.BooleanField(default=False)
    title = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Todo'
