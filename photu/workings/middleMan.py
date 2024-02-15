import time
from .githubHandler import GithubManager
from .repoSizeManager import RepoSizeManager
from .thumbnail import Thumbnail


class MiddleMan:
    def __init__(self,username) -> None:
        self.username=username
        self.git=GithubManager(username)
        self.thumb=Thumbnail()

    def upload_file(self,file):
        uname = str(int(time.time())) + '.' + file.name.split(".")[-1]
        fileContent=file.read()
        self.git.upload_file(self.thumb.create_thumbnail(fileContent),uname,'thumbnails')
        return uname, RepoSizeManager.upload(self.git,fileContent,uname,file.size),fileContent

    def download_file(self,filename,repo):
        return self.git.download_file(filename,repo)

    def delete_file(self,filename):
        pass

    def thumbnails(self,thumbnails_store):
        self.thumb.get_thumbnails(self.git,thumbnails_store)