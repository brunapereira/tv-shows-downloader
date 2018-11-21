import urllib.request
import os
from bs4 import BeautifulSoup
from external import pyaria2

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

    directory = create_directory(tv_show, version)

    # Add Magnet URL to Aria2 and get GID
    gid = pyaria2.PyAria2().addUri([magnet_link], dict(dir=directory))

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
        os.makedirs('tv-shows/' + tv_show + '-' + version)
        print("Directory", dir_name, "Created")
        return dir_name
    except FileExistsError:
        print("Directory", dir_name,  "already exists")
