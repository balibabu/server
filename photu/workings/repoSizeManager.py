from .repoMemory import RepoMemory
import time

class RepoSizeManager:

    def delete_file(filename):
        pass

    def get_free_repo(git,repoMem):
        repos=repoMem.get_repos()
        for repo in repos:
            if repoMem.get_size(repo)<= 419_430_400:
                return repo
        repo=str(int(time.time()))
        status=git.create_repo(repo)
        if status:
            return repo

    def upload(git,fileContent,filename,size):
        repoMem=RepoMemory('repMem.pkl')
        freeRepo=RepoSizeManager.get_free_repo(git,repoMem)
        if git.upload_file(fileContent,filename,freeRepo):
            repoMem.add_size(freeRepo,size)
            return freeRepo
        return False
        