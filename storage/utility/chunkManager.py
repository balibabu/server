class ChunkManagerForStorage:

    def __init__(self,data) -> None:
        self.size=int(data.get('size'))
        self.filename=data.get('filename')
        self.inside=data.get('inside')
        if self.inside=='null': self.inside=None
        self.receivedSize=0
        self.contents=[]

    def add_chunk(self,data,file):
        chunkIndex=int(data.get('chunkIndex'))
        content=file.read()
        self.contents.append((chunkIndex,content))
        self.receivedSize+=len(content)
    
    def is_completed(self):
        if self.receivedSize==self.size:
            return True
        return False

    def get_chunks(self):
        sorted_chunks = sorted(self.contents, key=lambda x: x[0])
        chunks = [item[1] for item in sorted_chunks]
        return chunks