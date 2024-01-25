import os,pickle

class MyDictionary:
    def __init__(self,filename='memory.pkl') -> None:
        self.filename=filename
        if not os.path.isfile(filename):
            with open(filename,'wb') as file:
                pickle.dump({},file)

        with open(filename, 'rb') as pklFile:
            self.data = pickle.load(pklFile)

    def get_size(self,key):
        return self.data.get(key,0)

    def add_size(self,key,value):
        if key in self.data:
            self.data[key]+=value
        else:
            self.data[key]=value
        self.save()
        

    def remove_size(self,key,value):
        self.data[key]-=value
        self.save()

    def add_repo(self,key,value):
        if key in self.data:
            self.data[key].append(value)
        else:
            self.data[key]=[value]
        self.save()
    def get_repos(self,key):
        return self.data.get(key,[])

    def save(self):
        with open(self.filename,'wb') as file:
            pickle.dump(self.data,file)