from django.db import models
from django.contrib.auth.models import User

class Storage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uploadedName=models.CharField(max_length=20)
    originalName=models.CharField(max_length=255)
    fileSize=models.FloatField()
    url=models.URLField()
    timestamp = models.DateTimeField(auto_now_add=True)
