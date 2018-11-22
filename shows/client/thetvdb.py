import requests
import json
from prettyconf import config


class TheTvDb(object):
    def __init__(self):
        self.base_url = 'https://api.thetvdb.com'
        self.api_key = config('TVDB_API_KEY')
        self.user_key = config('TVDB_USER_KEY')
        self.username = config('TVDB_USERNAME')
        self.token = None

    def login(self):
        data = {
            'apikey': self.api_key,
            'userkey': self.user_key,
            'username': self.username
        }

        headers = {'Content-Type': 'application/json'}

        response = requests.post(f'{self.base_url}/login', data=json.dumps(data), headers=headers)

        if (response.status_code == 200):
            self.token = f"Bearer {response.json()['token']}"
            print('Login successful')
        else:
            print ('some error occurred')

    def fetch_favorites_from_user(self):
        headers = {'Authorization': self.token}
        response = requests.get(f'{self.base_url}/user/favorites', headers=headers)

        if (response.status_code == 200):
            return response.json()['data']['favorites']
        else:
            print ('some error occurred')
    
    def get_tv_show_name(self, tv_show_id):
        headers = {'Authorization': self.token}
        response = requests.get(f'{self.base_url}/series/{tv_show_id}', headers=headers)

        if (response.status_code == 200):
            return response.json()['data']['seriesName']
        else:
            print ('some error occurred')

    def find_last_episode(self, tv_show_id):
        response = self.fetch_episodes(tv_show_id)
        last_page = response.json()['links']['last']

        last_aired = self.fetch_episodes(tv_show_id, last_page).json()['data'][-1]
        season = last_aired['airedSeason'] 
        episode = str(last_aired['airedEpisodeNumber']).zfill(2)

        return f'S{season}E{episode}'

    def fetch_episodes(self, tv_show_id, page=1):
        headers = {'Authorization': self.token}

        return requests.get(f'{self.base_url}/series/{tv_show_id}/episodes/query?page={page}', headers=headers)

if __name__ == '__main__':
    client = TheTvDb()
    client.login()
    client.fetch_favorites_from_user()
    client.find_last_episode('73762')
    client.get_tv_show_name('73762')
