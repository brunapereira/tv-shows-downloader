from external import pyaria2
import time

def download_at(directory, magnet_link):
    download_status = ''
    aria2c = pyaria2.PyAria2()
    
    # Add Magnet URL to Aria2 and get GID
    gid = aria2c.addUri([magnet_link], dict(dir=directory))
    print('Downloading.')

    while download_status != 'complete':
        download_status = aria2c.tellStatus(gid, ['status'])['status']
        print('.')
        time.sleep(1)

    print(download_status)

    return True
