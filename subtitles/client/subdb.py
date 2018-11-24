import glob
import os
import requests

from models import File

API_URL_BASE = 'http://api.thesubdb.com/'

def fetch_subtitle(video_file):
    content = fetch(video_file.get_hash())

    # TODO: Check if the file already exists
    if content:
        subtitle_file = open(video_file.directory + '/' + video_file.name + '.srt', 'w')
        subtitle_file.write(content)

def fetch(video_hash):
    url = '{0}?action=download&hash={1}&language=pt,en'.format(API_URL_BASE, video_hash)

    headers = requests.utils.default_headers()
    headers.update(
        {
            'User-Agent': 'SubDB/1.0 (tv-shows-downloader/0.1; https://github.com/brunapereira/tv-shows-downloader)',
        }
    )

    response = requests.get(url, headers=headers)
    if (response.status_code == 200):
        return response.content.decode('ISO-8859-1')
    else:
        print ('Some error occurred! Error code:', response.status_code)
