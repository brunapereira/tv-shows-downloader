import hashlib
import os

class File():
    def __init__(self, path):
        self.path = path
        self.directory = os.path.splitext(path.rsplit('/',1)[0])[0]
        self.name = os.path.splitext(path.rsplit('/',1)[1])[0]
        self.extension = os.path.splitext(path.rsplit('/',1)[1])[1]

    def get_name_with_extension(self):
        return self.name + self.extension

    def move_to(self, root_directory):
        new_path = root_directory + '/' + self.name + self.extension
        os.rename(self.path, new_path)
        return File(new_path)

    def get_hash(self):
        readsize = 64 * 1024
        with open(self.path, 'rb') as f:
            size = os.path.getsize(self.path)
            data = f.read(readsize)
            f.seek(-readsize, os.SEEK_END)
            data += f.read(readsize)
        return hashlib.md5(data).hexdigest()

