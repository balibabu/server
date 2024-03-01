from django.db import models

class FileInfo(models.Model):
    name=models.CharField(max_length=255)
    size = models.FloatField()

class Chunk(models.Model):
    fileInfo=models.ForeignKey(FileInfo,on_delete=models.CASCADE)
    repo=models.CharField(max_length=12)
    uname=models.CharField(max_length=12)
    size = models.FloatField()
    
class RepoSize(models.Model):
    name = models.CharField(max_length=255, unique=True)
    size = models.IntegerField(default=0)
    def __str__(self):
        return self.name
    def add_size(self, size):
        self.size += size
        self.save()
    def remove_size(self, size):
        self.size -= size
        self.save()
    @classmethod
    def get_size(cls, repo_name):
        try:
            repo = cls.objects.get(name=repo_name)
            return repo.size
        except cls.DoesNotExist:
            return 0
    @classmethod
    def get_repos(cls):
        return cls.objects.all().values_list('name', flat=True)
