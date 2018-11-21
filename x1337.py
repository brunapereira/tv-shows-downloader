import urllib2
from bs4 import BeautifulSoup
import pyaria2

BASE_URL = 'https://1337x.to'

def download(tv_show, version):
    search_string = '%s %s' % (tv_show, version)
    search_string = search_string.replace(' ', '%20')

    uri = '/search/' + search_string + '//'

    # Search for a tv show
    search_page_object = create_page_object(uri)

    # Find URI to first result
    uri_to_episode_page = find_uri_to_episode_page(search_page_object)

    # Open episode page
    episode_page_object = create_page_object(uri_to_episode_page)

    # Extract magnet link
    magnet_link = find_magnet_link(episode_page_object)
    print(magnet_link)

    pyaria2.PyAria2().addUri(magnet_link)

def find_uri_to_episode_page(page):
    return page.find('td', { 'class': 'coll-1 name' }).find('a', { 'class': None })['href']
    
def find_magnet_link(page):
    return page.select_one('a[href*=magnet]')['href'] 

def create_page_object(uri):
    request = urllib2.Request(BASE_URL + uri, headers={ 'User-Agent': 'Mozilla/5.0' })
    html_string = urllib2.urlopen(request).read()

    return BeautifulSoup(html_string, features="html.parser")
