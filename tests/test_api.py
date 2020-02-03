from datetime import datetime

import pytest

from avri import api
from avri.api import Cache, Garbage


@pytest.fixture
def fake_response():
    return """GFT;04-02-2020;21-01-2020;07-01-2020;
PLASTIC;03-02-2020;13-01-2020;
PAPIER;04-02-2020;07-01-2020;
"""


@pytest.fixture
def client_with_cache(fake_response):
    client = api.Avri('1234AB', '42')
    client._cache = Cache(client.parse_content(fake_response), datetime.now())
    return client


def test_parse_content(fake_response):
    client = api.Avri('1234AB', '42')
    data = client.parse_content(fake_response).list()
    assert len(data) == 7
    assert len([_ for _ in data if _.name == 'gft']) == 3
    assert len([_ for _ in data if _.name == 'plastic']) == 2
    assert len([_ for _ in data if _.name == 'papier']) == 2


def test_upcoming_new(client_with_cache):
    assert client_with_cache.upcoming(datetime(2020, 1, 6)) == Garbage('gft', datetime(2020, 1, 7))


def test_upcoming_today(client_with_cache):
    assert client_with_cache.upcoming(datetime(2020, 1, 7)) == Garbage('gft', datetime(2020, 1, 7))


def test_upcoming_of_each_new(client_with_cache):
    assert client_with_cache.upcoming_of_each(datetime(2020, 1, 6)) == [
        Garbage('gft', datetime(2020, 1, 7)),
        Garbage('papier', datetime(2020, 1, 7)),
        Garbage('plastic', datetime(2020, 1, 13))
    ]


def test_upcoming_of_each_today(client_with_cache):
    assert client_with_cache.upcoming_of_each(datetime(2020, 1, 7)) == [
        Garbage('gft', datetime(2020, 1, 7)),
        Garbage('papier', datetime(2020, 1, 7)),
        Garbage('plastic', datetime(2020, 1, 13))
    ]
