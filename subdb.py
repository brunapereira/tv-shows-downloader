import glob
import os
import requests

from File import File

API_URL_BASE = 'http://api.thesubdb.com/'

def get_subtitle(directory):
    # TODO: Accept multiple extensions
    for path in glob.iglob(directory + '/**/*.mkv', recursive=True):
        video_file = File(path)

    content = fetch_subtitle(video_file.get_hash())

    # TODO: Check if the file already exists
    subtitle_file = open(directory + '/' + video_file.name + '.srt', 'w')
    subtitle_file.write(content)

def fetch_subtitle(video_hash):
    url = '{0}?action=download&hash={1}&language=pt,en'.format(API_URL_BASE, video_hash)

    headers = requests.utils.default_headers()
    headers.update(
        {
            'User-Agent': 'SubDB/1.0 (tv-shows-downloader/0.1; https://github.com/brunapereira/tv-shows-downloader)',
        }
    )

    response = requests.get(url, headers=headers)
    if (response.status_code == 200):
        return response.content.decode('utf-8')
    else:
        print ('Some error occurred! Error code:', response.status_code)
