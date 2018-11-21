import hashlib
import os

class File():
    def __init__(self, path):
        self.path = path
        self.name = os.path.splitext(path.rsplit('/',1)[1])[0]

    def get_hash(self):
        readsize = 64 * 1024
        with open(self.path, 'rb') as f:
            size = os.path.getsize(self.path)
            data = f.read(readsize)
            f.seek(-readsize, os.SEEK_END)
            data += f.read(readsize)
        return hashlib.md5(data).hexdigest()

