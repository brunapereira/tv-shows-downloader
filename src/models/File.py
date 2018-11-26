import hashlib
import os

class File():
    def __init__(self, path):
        self.directory, self.name_with_extension = path.rsplit('/',1)
        self.path = path
        self.name = os.path.splitext(self.name_with_extension)[0]

    def move_to(self, root_directory):
        new_path = root_directory + self.name_with_extension
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
