from github import Github
import base64

class GithubManager:
    def __init__(self,username) -> None:
        file=open('gitToken.env')
        tk=file.read()
        self.git=Github(tk)
        self.username=username

    def upload_file(self,fileContent,filename,repo_name):
        repo = self.git.get_repo("storeage/"+repo_name)
        file_path_in_repo=f'{self.username}/{filename}'
        repo.create_file(
            path=file_path_in_repo,
            message='uploaded '+filename,
            content=fileContent,
        )

    def download_file(self,filename,repo_name):
        repo = self.git.get_repo("storeage/"+repo_name)
        file = repo.get_contents(f'{self.username}/{filename}')
        blob_content = repo.get_git_blob(file.sha).content
        content_bytes = base64.b64decode(blob_content)
        return content_bytes

    def create_repo(self,repo_name):
        user=self.git.get_user()
        user.create_repo(repo_name,private=True)
    
    def delete_file(self,filename,repo_name):
        repo = self.git.get_repo("storeage/"+repo_name)
        file = repo.get_contents(f"{self.username}/{filename}")
        sha = file.sha
        repo._requester.requestJsonAndCheck(
            "DELETE",
            f"/repos/storeage/{repo_name}/contents/{self.username}/{filename}",
            input={
                "message": f"Delete {filename} completely",
                "sha": sha,
                "branch": 'main'
            }
        )
    
    