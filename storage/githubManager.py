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

# https://raw.githubusercontent.com/[gituser]/[repo-name]/main/[username/foldername]/[filename]
            # file_url = f"https://github.com/{self.repo_owner}/{self.repo_name}/blob/{self.branch_name}/{file_path_in_repo}"
            # file_url = f"https://github.com/{self.repo_owner}/{self.repo_name}/blob/{self.branch_name}/{file_path_in_repo}"
            return file_name
        except Exception as e:
            print(f"Error uploading file: {e}")
            return False
        
    def get_file_content(self, file_path_in_repo):
        try:
            repo = self.g.get_repo(f"{self.repo_owner}/{self.repo_name}")
            file_content = repo.get_contents(file_path_in_repo, ref=self.branch_name).decoded_content
            return file_content
        except Exception as e:
            print(f"Error fetching file content: {e}")
            return None

        