from django.db import models

class Link(models.Model):
    full_link=models.TextField()

    def __str__(self):
        return self.full_link
    

from rest_framework import serializers
class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = '__all__'