import vcr
import pytest


from shows.client.thetvdb import TheTvDb


@pytest.fixture()
def client():
    return TheTvDb()


@vcr.use_cassette('shows/client/tests/fixtures/thetvdb/vcr/login.yml')
def test_login(client):
    client.login()
    assert client.token


@vcr.use_cassette('shows/client/tests/fixtures/thetvdb/vcr/favorites.yml')
def test_get_info_from_favorites(client):
    client.login()
    assert client.get_info_from_favorites() is None


@vcr.use_cassette('shows/client/tests/fixtures/thetvdb/vcr/fetch_favorites.yml')
def test_fetch_favorites_from_user(client):
    client.login()
    response = client.fetch_favorites_from_user()
    assert len(response) > 0


@vcr.use_cassette('shows/client/tests/fixtures/thetvdb/vcr/get_tv_show_name.yml')
def test_get_tv_show_name(client):
    client.login()
    response = client.get_tv_show_name(73762)
    assert len(response) > 0
