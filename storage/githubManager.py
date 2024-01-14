import base64
from github import Github
import time

class GithubManager:
    def __init__(self, token,repo_owner,repo_name,folder_name):
        self.g = Github(token)
        self.repo_owner = repo_owner 
        self.repo_name = repo_name
        self.folder_name=folder_name
        self.branch_name = "main" 
    
    def delete_image_completely(self, file_name):
        try:
            repo = self.g.get_repo(f"{self.repo_owner}/{self.repo_name}")
            existing_file = repo.get_contents(f"{self.folder_name}/{file_name}", ref=self.branch_name)
            sha = existing_file.sha
            repo._requester.requestJsonAndCheck(
                "DELETE",
                f"/repos/{self.repo_owner}/{self.repo_name}/contents/{self.folder_name}/{file_name}",
                input={
                    "message": f"Delete {file_name} completely",
                    "sha": sha,
                    "branch": self.branch_name
                }
            )
            print(f"File '{file_name}' deleted completely.")
            return True
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False

    def upload_in_memory_file(self, in_memory_file):
        try:
            repo = self.g.get_repo(f"{self.repo_owner}/{self.repo_name}")

            file_content = in_memory_file.read()

            extension = in_memory_file.name.split(".")[-1]
            file_name = str(int(time.time())) + '.' + extension
            file_path_in_repo = f"{self.folder_name}/{file_name}"

            repo.create_file(
                path=file_path_in_repo,
                message=f"Upload {file_name}",
                content=file_content,
                branch=self.branch_name
            )
            return True,file_name
        except Exception as e:
            print(f"Error uploading file: {e}")
            return False,e
        
    def get_file_content(self, filename):
        try:
            repo = self.g.get_repo(f"{self.repo_owner}/{self.repo_name}")
            branch_ref = repo.get_branch(self.branch_name)
            commit = repo.get_commit(branch_ref.commit.sha)
            tree = repo.get_git_tree(commit.sha, recursive=True)
            blob_sha = None
            filepath=f'{self.folder_name}/{filename}'
            for entry in tree.tree:
                if entry.path == filepath:
                    blob_sha = entry.sha
                    break
            if blob_sha:
                blob_content = repo.get_git_blob(blob_sha).content
                content_bytes = base64.b64decode(blob_content)
                return True,content_bytes
            else:
                return False, 'file not found'
        except Exception as e:
            return False, e


    def create_repo(self,repo_name):
        try:
            user=self.g.get_user()
            new_repo=user.create_repo(repo_name,private=True)
            return True
        except Exception as e:
            print(e)
            return False