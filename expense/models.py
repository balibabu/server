from django.contrib.auth.models import User
from django.db import models

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    amount = models.IntegerField()
    note = models.CharField(max_length=255, default="")
