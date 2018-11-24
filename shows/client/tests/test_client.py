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
