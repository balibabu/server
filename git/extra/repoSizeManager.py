from git.models import RepoSize
import time
from .config import MAX_GIT_REPO_SIZE
from .githubManager import GithubManager

class RepoSizeManager:

    def _get_repos():
        return list(RepoSize.get_repos())

    def _get_size(repo):
        return RepoSize.get_size(repo)

    def add_size(repo, size):
        repo_obj, created = RepoSize.objects.get_or_create(name=repo)
        repo_obj.size += size
        repo_obj.save()

    def remove_size(repo, size):
        try:
            repo_obj = RepoSize.objects.get(name=repo)
            repo_obj.size -= size
            repo_obj.save()
        except RepoSize.DoesNotExist:
            pass

    def get_free_repo():
        repos=RepoSizeManager._get_repos()
        for repo in repos:
            if RepoSizeManager._get_size(repo)<= MAX_GIT_REPO_SIZE: #400MB
                return repo
        repo=str(int(time.time()))
        git=GithubManager('dummy')
        git.create_repo(repo)
        return repo
    