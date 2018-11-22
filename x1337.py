import urllib.request
import os
import glob
from File import File
import subdb
import aria2c
from bs4 import BeautifulSoup

BASE_URL = 'https://1337x.to'
BASE_TV_SHOWS_DIR = 'tv-shows/'

def download(tv_show, version):
    search_string = '%s %s' % (tv_show, version)
    search_string = search_string.replace(' ', '%20')

    uri_search = '/search/' + search_string + '//'

    # Search for a tv show
    search_page_object = create_page_object(uri_search)

    # Find URI to first result
    uri_to_episode_page = find_uri_to_episode_page(search_page_object)

    # Open episode page
    episode_page_object = create_page_object(uri_to_episode_page)

    # Extract magnet link
    magnet_link = find_magnet_link(episode_page_object)

    # Create dir
    directory = create_directory(tv_show, version)

    # Download Video
    # aria2c.download_at(directory, magnet_link)

    # Move video to correct folder
    video_file = move_video(directory)

    # Download subtitle
    subdb.get_subtitle(video_file)

def find_uri_to_episode_page(page):
    return page.find('td', { 'class': 'coll-1 name' }).find('a', { 'class': None })['href']
    
def find_magnet_link(page):
    return page.select_one('a[href*=magnet]')['href'] 

def create_page_object(uri):
    request = urllib.request.Request(BASE_URL + uri, headers={ 'User-Agent': 'Mozilla/5.0' })
    html_string = urllib.request.urlopen(request).read()

    return BeautifulSoup(html_string, features="html.parser")

def create_directory(tv_show, version):
    dir_name = BASE_TV_SHOWS_DIR + tv_show + '-' + version

    try:
        os.makedirs(dir_name)
        print("Directory", dir_name, "Created")
    except FileExistsError:
        print("Directory", dir_name,  "already exists")

    return dir_name

def move_video(directory):
    # TODO: Accept multiple extensions
    for path in glob.iglob(directory + '/**/*.mkv', recursive=True):
        video_file = File(path)
    
    return video_file.move_to(directory)
