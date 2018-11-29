import vcr
import pytest

from shows.client.thetvdb import TheTvDb


@pytest.fixture()
def client():
    with vcr.use_cassette('src/shows/client/tests/fixtures/thetvdb/vcr/login.yml'):
        return TheTvDb()


def test_login(client):
    assert client.token


@vcr.use_cassette('src/shows/client/tests/fixtures/thetvdb/vcr/fetch_favorites.yml')
def test_fetch_favorites_from_user(client):
    response = client.fetch_favorites_from_user()
    assert len(response) > 0


@vcr.use_cassette('src/shows/client/tests/fixtures/thetvdb/vcr/get_tv_show_name.yml')
def test_get_tv_show_name(client):
    response = client.get_tv_show_name(73762)
    assert len(response) > 0


@vcr.use_cassette('src/shows/client/tests/fixtures/thetvdb/vcr/find_last_episode.yml')
def test_find_last_episode(client):
    response = client.find_last_episode(73762)
    assert response == "S15E08"


@vcr.use_cassette('src/shows/client/tests/fixtures/thetvdb/vcr/fetch_episodes.yml')
def test_fetch_episodes(client):
    response = client.fetch_episodes(73762, 4)
    assert response.json() is not None


@vcr.use_cassette('src/shows/client/tests/fixtures/thetvdb/vcr/find_last_released_episode.yml')
def test_find_last_released_episode(client):
    last_episodes = client.fetch_episodes(73762, 4).json()['data']
    response = client.find_last_released_episode(last_episodes)
    assert response['id']
