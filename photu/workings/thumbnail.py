from PIL import Image
from io import BytesIO

class Thumbnail:
    def __init__(self) -> None:
        pass

    def create_thumbnail(self,file_data, size=(128, 128)):
        try:
            with Image.open(BytesIO(file_data)) as img:
                img.thumbnail(size)
                thumbnail_buffer = BytesIO()
                img.save(thumbnail_buffer,img.format)
            return thumbnail_buffer.getvalue()
        except Exception as e:
            print(f"Error creating thumbnail: {e}")
            return None
    
    def get_thumbnails(self,git):
        return git.download_thumbnail()