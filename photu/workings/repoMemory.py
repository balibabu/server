import os,pickle

class RepoMemory:
    def __init__(self,filename='repo.pkl') -> None:
        self.filename=filename
        if not os.path.isfile(filename):
            with open(filename,'wb') as file:
                pickle.dump({},file)

        with open(filename, 'rb') as pklFile:
            self.data = pickle.load(pklFile)

    def save(self):
        with open(self.filename,'wb') as file:
            pickle.dump(self.data,file)

    def get_size(self,repo):
        return self.data.get(repo,0)

    def add_size(self,repo,size):
        if repo in self.data:
            self.data[repo]+=size
        else:
            self.data[repo]=size
        self.save()

    def remove_size(self,repo,size):
        self.data[repo]-=size
        self.save()
    
    def get_repos(self):
        return list(self.data.keys())
    