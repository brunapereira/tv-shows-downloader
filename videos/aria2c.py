from pyaria2 import Aria2RPC
import time

aria2c = Aria2RPC()

def download_at(directory, magnet_link):
    # Add Magnet URL to Aria2 and get Metalink GID
    gid_metalink = aria2c.addUri(uris=[magnet_link], options=dict(dir=directory))
    print('Downloading metalink.')
    wait_for_download(gid_metalink)

    # When Metalink is downloaded, get first GID created from metalink (the video)
    gid_video = aria2c.tellStatus(gid_metalink)['followedBy'][0]
    print('Downloading video.')
    wait_for_download(gid_video)

def wait_for_download(gid):
    status = ''
    while status != 'complete':
        video_status = aria2c.tellStatus(gid)['status']
        time.sleep(1)
