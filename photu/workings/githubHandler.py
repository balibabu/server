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

    def delete_file(filename):
        pass

    def download_thumbnail(self,thumbnails_store):
        repo = self.git.get_repo("storeage/thumbnails")
        folder_contents = repo.get_contents(self.username)
        for item in folder_contents:
            if item.name not in thumbnails_store:
                thumbnails_store[item.name]=item.decoded_content
                print('not')
            else:
                print('yes')


    def create_repo(self,repo):
        try:
            user=self.git.get_user()
            user.create_repo(repo,private=True)
            return True
        except Exception as e:
            print(e)
            return False