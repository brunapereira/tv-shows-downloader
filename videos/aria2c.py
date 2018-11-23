from pyaria2 import Aria2RPC
import time

def download_at(directory, magnet_link):
    aria2c = Aria2RPC()
    download_status = ''
    
    # Add Magnet URL to Aria2 and get GID
    gid = aria2c.addUri(uris=[magnet_link], options=dict(dir=directory))
    print('Downloading.')

    while download_status != 'complete':
        download_status = aria2c.tellStatus(gid)['status']
        print('.')
        time.sleep(1)

    return True
