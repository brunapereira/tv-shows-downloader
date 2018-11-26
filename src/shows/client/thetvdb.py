import requests
import json
import sys
from prettyconf import config
from dateutil import parser
from datetime import datetime
from repository.client import redis


class TheTvDb(object):
    def __init__(self):
        self.base_url = 'https://api.thetvdb.com'
        self.api_key = config('TVDB_API_KEY')
        self.user_key = config('TVDB_USER_KEY')
        self.username = config('TVDB_USERNAME')
        self.token = self.login()

    def handle_response(self, response):
        if response.status_code != 200:
            print ('some error occurred %s:' % (response.text))
            sys.exit(1)

    def login(self):
        data = {
            'apikey': self.api_key,
            'userkey': self.user_key,
            'username': self.username}

        headers = {'Content-Type': 'application/json'}

        uri = '{}/login'.format(self.base_url)
        response = requests.post(uri, data=json.dumps(data), headers=headers)

        self.handle_response(response)

        return 'Bearer %s' % (response.json()['token'])

    def fetch_favorite_shows(self):
        favorites = self.fetch_favorites_from_user()

        for favorite in favorites:
            last_episode = self.find_last_episode(favorite)
            name = self.get_tv_show_name(favorite)

            redis.save(favorite, 'last_episode', last_episode)
            redis.save(favorite, 'name', name)

    def fetch_favorites_from_user(self):
        headers = {'Authorization': self.token}
        uri = '{}/user/favorites'.format(self.base_url)
        response = requests.get(uri, headers=headers)

        self.handle_response(response)
        return response.json()['data']['favorites']

    def get_tv_show_name(self, tv_show_id):
        headers = {'Authorization': self.token}
        uri = '{}/series/{}'.format(self.base_url, tv_show_id)
        response = requests.get(uri, headers=headers)

        self.handle_response(response)
        return response.json()['data']['seriesName']

    def find_last_episode(self, tv_show_id):
        episodes = self.fetch_episodes(tv_show_id)
        last_page = episodes.json()['links']['last']
        last_episodes = self.fetch_episodes(tv_show_id, last_page).json()['data']

        last_released = self.find_last_released_episode(last_episodes)

        season = str(last_released['airedSeason']).zfill(2)
        episode = str(last_released['airedEpisodeNumber']).zfill(2)

        return 'S{}E{}'.format(season, episode)

    def find_last_released_episode(self, episodes):
        current_day = datetime.now()

        for episode in episodes:
            first_aired = parser.parse(episode['firstAired'])

            if ((current_day - first_aired).days >= 2):
                return episode



    def fetch_episodes(self, tv_show_id, page=1):
        headers = {'Authorization': self.token}

        uri = '{}/series/{}/episodes/query?page={}'.format(self.base_url, tv_show_id, page)
        response = requests.get(uri, headers=headers)
        self.handle_response(response)
        return response


if __name__ == '__main__':
    client = TheTvDb()
    client.login()
    client.fetch_favorites_from_user()
    client.find_last_episode('73762')
    client.get_tv_show_name('73762')
