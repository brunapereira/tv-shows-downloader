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



if __name__ == '__main__':

    client = TheTvDb()
    client.login()
    client.fetch_favorites_from_user()
