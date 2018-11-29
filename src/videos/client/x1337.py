import urllib.request
from bs4 import BeautifulSoup
from prettyconf import config

BASE_URL = config('X1337_BASE_URL')

def fetch_magnet_link(tv_show, version):
    search_string = '{0} {1}'.format(tv_show, version).replace(' ', '%20')
    uri_search = '/search/{0}//'.format(search_string)

    # Search for a tv show
    search_page_object = create_page_object(uri_search)

    # Find URI to first result
    uri_to_episode_page = find_uri_to_episode_page(search_page_object)

    # Open episode page
    episode_page_object = create_page_object(uri_to_episode_page)

    # Extract magnet link
    return find_magnet_link(episode_page_object)

def find_uri_to_episode_page(page):
    return page.find('td', { 'class': 'coll-1 name' }).find('a', { 'class': None })['href']
    
def find_magnet_link(page):
    return page.select_one('a[href*=magnet]')['href'] 

def create_page_object(uri):
    request = urllib.request.Request(BASE_URL + uri, headers={ 'User-Agent': 'Mozilla/5.0' })
    html_string = urllib.request.urlopen(request).read()

    return BeautifulSoup(html_string, features="html.parser")
