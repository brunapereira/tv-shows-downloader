from pyaria2 import Aria2RPC
import time
import sys
import subprocess
import os

aria2c = Aria2RPC()

def start():
    if not isAria2Installed():
        print('Aria 2 is not installed')
        sys.exit(0)

    if not isAria2rpcRunning():
        cmd = 'aria2c' \
              ' --enable-rpc' \
              ' --continue' \
              ' --max-concurrent-downloads=20' \
              ' --max-connection-per-server=10' \
              ' --allow-overwrite=true' \
              ' --seed-time=0' \
              ' --rpc-max-request-size=1024M'

        subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

        count = 0
        while True:
            if isAria2rpcRunning():
                break
            else:
                count += 1
                time.sleep(3)
            if count == 5:
                raise Exception('aria2 RPC server started failure.')
        print('aria2 RPC server is started.')
    else:
        print('aria2 RPC server is already running.')


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
        status = aria2c.tellStatus(gid)['status']
        time.sleep(1)

def isAria2Installed():
    for cmdpath in os.environ['PATH'].split(':'):
        if os.path.isdir(cmdpath) and 'aria2c' in os.listdir(cmdpath):
            return True

    return False

def isAria2rpcRunning():
    pgrep_process = subprocess.Popen('pgrep -l aria2', shell=True, stdout=subprocess.PIPE)

    if pgrep_process.stdout.readline() == b'':
        return False
    else:
        return True
