from django.db import models
from django.contrib.auth.models import User

class Photo(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    oname=models.CharField(max_length=255)
    uname=models.CharField(max_length=20)
    size = models.FloatField()

class Repo(models.Model):
    photo=models.ForeignKey(Photo,on_delete=models.CASCADE)
    repo=models.CharField(max_length=20)