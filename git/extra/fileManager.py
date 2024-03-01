from git.models import FileInfo, Chunk
from .githubManager import GithubManager
from .repoSizeManager import RepoSizeManager
from django.db import transaction
import time

class FileManager:

    def __init__(self,username) -> None:
        self.git=GithubManager(username)
    
    def upload(self, chunks, name):
        fileInfo = None
        chunk_uname_size = []
        repo=RepoSizeManager.get_free_repo()
        with transaction.atomic():
            fileInfo = FileInfo.objects.create(name=name, size=sum(map(len,chunks)))
            for chunk in chunks:
                uname=str(int(time.time()))
                self.git.upload_file(chunk,uname,repo)
                chunk_uname_size.append((uname,len(chunk)))
            
            for uname,size in chunk_uname_size:
                Chunk.objects.create(fileInfo=fileInfo,repo=repo,uname=uname,size=size)
        RepoSizeManager.add_size(repo,fileInfo.size)
        return fileInfo

    def delete(self,fileInfo):
        chunks=Chunk.objects.filter(fileInfo=fileInfo)
        for chunk in chunks:
            self.git.delete_file(chunk.uname,chunk.repo)
            RepoSizeManager.remove_size(chunk.repo, chunk.size)
        fileInfo.delete()

    def download(self,fileInfo):
        fileContent=b''
        chunks=Chunk.objects.filter(fileInfo=fileInfo) #assuming chunks are sorted by id
        for chunk in chunks:
            fileContent+=self.git.download_file(chunk.uname,chunk.repo)
        return fileContent
        
        
