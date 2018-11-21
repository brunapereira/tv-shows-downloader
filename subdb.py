import glob
import os
import hashlib
import requests

API_URL_BASE = 'http://api.thesubdb.com/'

def get_subtitle(directory):
    # TODO: Accept multiple extensions
    for _file in glob.iglob(directory + '/**/*.mkv', recursive=True):
        file_path = _file
        filename = _file.rsplit('/',1)[1]

    video_hash = get_hash(file_path)

    content = fetch_subtitle(video_hash)

    subtitle_file = open(directory + 'testfile.srt', 'w')
    subtitle_file.write(content)) 

def fetch_subtitle(video_hash):
    url = '{0}?action=download&hash={1}&language=pt,en'.format(API_URL_BASE, video_hash)

    headers = requests.utils.default_headers()
    headers.update(
        {
            'User-Agent': 'SubDB/1.0 (tv-shows-downloader/0.1; https://github.com/brunapereira/tv-shows-downloader)',
        }
    )

    response = requests.get(url, headers=headers)

    return response.content.decode('utf-8')

def get_hash(name):
    readsize = 64 * 1024
    with open(name, 'rb') as f:
        size = os.path.getsize(name)
        data = f.read(readsize)
        f.seek(-readsize, os.SEEK_END)
        data += f.read(readsize)
    return hashlib.md5(data).hexdigest()

