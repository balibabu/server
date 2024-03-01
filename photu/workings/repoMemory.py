from git.models import RepoSize 

class RepoMemory:

    def get_size(self, repo):
        return RepoSize.get_size(repo)

    def add_size(self, repo, size):
        repo_obj, created = RepoSize.objects.get_or_create(name=repo)
        repo_obj.size += size
        repo_obj.save()

    def remove_size(self, repo, size):
        try:
            repo_obj = RepoSize.objects.get(name=repo)
            repo_obj.size -= size
            repo_obj.save()
        except RepoSize.DoesNotExist:
            pass

    def get_repos(self):
        return list(RepoSize.get_repos())
