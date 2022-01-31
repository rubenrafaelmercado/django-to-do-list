from .list_statuses import LIST_STATUSES
from django.db import models
from django.contrib.auth.models import User



class Task(models.Model):

    name = models.CharField(max_length=50)
    status = models.CharField(max_length=1, default='T', choices=LIST_STATUSES)
    due_date_time = models.DateTimeField()
    description = models.CharField(max_length=300)
    comment = models.CharField(max_length=400)
    user = models.ForeignKey(User, on_delete=models.CASCADE)    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

