from django.db import models
from django.contrib.auth.models import User

class GithubInfo(models.Model):
    repo_owner = models.CharField(max_length=255)
    repo_name = models.CharField(max_length=255)
    token = models.CharField(max_length=40)

class Storage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uploadedName = models.CharField(max_length=20)
    originalName = models.CharField(max_length=255)
    fileSize = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    github = models.ForeignKey(GithubInfo, on_delete=models.CASCADE, null=True)
