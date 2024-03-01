from github import Github
import base64

class GithubManager:
    def __init__(self,username) -> None:
        file=open('gitToken.env')
        tk=file.read()
        self.git=Github(tk)
        self.username=username

    def upload_file(self,fileContent,uname,repo): # uname is unique uploaded name
        try:
            repo = self.git.get_repo("storeage/"+repo)
            file_path_in_repo=f'{self.username}/{uname}'
            repo.create_file(
                path=file_path_in_repo,
                message='uploaded '+uname,
                content=fileContent,
            )
            return True
        except Exception as e:
            print(e)
            return False

    def download_file(self,filename,repo):
        repo = self.git.get_repo("storeage/"+repo)
        file = repo.get_contents(f'{self.username}/{filename}')
        blob_content = repo.get_git_blob(file.sha).content
        content_bytes = base64.b64decode(blob_content)
        return content_bytes

    def download_thumbnail(self,thumbnails_store):
        repo = self.git.get_repo("storeage/thumbnails")
        folder_contents = repo.get_contents(self.username)
        for item in folder_contents:
            if item.name not in thumbnails_store:
                thumbnails_store[item.name]=item.decoded_content

    def create_repo(self,repo):
        try:
            user=self.git.get_user()
            user.create_repo(repo,private=True)
            return True
        except Exception as e:
            print(e)
            return False

    def delete_file(self,uname,repo):
        try:
            repo = self.git.get_repo("storeage/"+repo)
            file = repo.get_contents(f"{self.username}/{uname}")
            sha = file.sha
            repo._requester.requestJsonAndCheck(
                "DELETE",
                f"/repos/storeage/{repo}/contents/{self.username}/{uname}",
                input={
                    "message": f"Delete {uname} completely",
                    "sha": sha,
                    "branch": 'main'
                }
            )
            self.delete_thumbnail(uname)
            return True
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False

    def delete_thumbnail(self,uname):
        repo = self.git.get_repo("storeage/thumbnails")
        file = repo.get_contents(f"{self.username}/{uname}")
        sha = file.sha
        repo._requester.requestJsonAndCheck(
            "DELETE",
            f"/repos/storeage/{repo}/contents/{self.username}/{uname}",
            input={
                "message": f"Delete {uname} completely",
                "sha": sha,
                "branch": 'main'
            }
        )