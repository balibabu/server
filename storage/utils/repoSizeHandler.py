from .myDictionary import MyDictionary
from .githubManager import GithubManager

class RepoSizeHandler:

    def __init__(self,token,folder_name) -> None:
        self.gitSizeLimit=419_430_400 # Bytes or 400 MB
        self.obj=MyDictionary('memory.pkl')
        self.obj2=GithubManager(token,folder_name)
    
    def get_free_repo(self,repo_owner):
        repos=self.obj.get_repos(repo_owner)
        for repo in repos:
            if self.obj.get_size((repo_owner,repo))<=self.gitSizeLimit:
                return repo
        new_repo=self.obj2.create_repo()
        if new_repo: self.obj.add_repo(repo_owner,new_repo)
        return new_repo

    def upload_file(self,repo_owner,repo_name,file):
        status,uploaded_filename=self.obj2.upload_in_memory_file(repo_owner,repo_name,file)
        if status: self.obj.add_size((repo_owner,repo_name),file.size)
        return status,uploaded_filename
    
    def delete_file(self,repo_owner,repo_name,file_name,size):
        status=self.obj2.delete_image_completely(repo_owner,repo_name,file_name)
        if status: self.obj.remove_size((repo_owner,repo_name),size)
        return status

    def get_repo_size(self,repo_owner,repo_name):
        print(self.obj.get_size((repo_owner,repo_name)))