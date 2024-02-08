from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    important = models.BooleanField()
    completed = models.BooleanField(default=False)
    datecompleted = models.DateTimeField(null=True, blank=True, auto_now_add=False)
