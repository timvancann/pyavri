import json
from datetime import datetime

import pytest
import requests_mock

from avri import api
from avri.api import Cache, Garbage
from avri.endpoints import BASE_URL, FETCH_ADDRESS


@pytest.fixture
def fake_calendar():
    return {
        "dataList": [
            {
                "pickupDates": [
                    "2021-01-21T00:00:00",
                    "2021-02-04T00:00:00",
                ],
                "pickupType": 1,
                "_pickupTypeText": "GREEN",
            },
            {
                "pickupDates": [
                    "2021-02-02T00:00:00",
                    "2021-03-02T00:00:00",
                    "2021-04-06T00:00:00",
                ],
                "pickupType": 2,
                "_pickupTypeText": "PAPER",
            },
            {
                "pickupDates": [
                    "2021-02-09T00:00:00",
                    "2021-03-02T00:00:00",
                    "2021-03-23T00:00:00",
                ],
                "pickupType": 10,
                "_pickupTypeText": "PACKAGES",
            }
        ],
    }


@pytest.fixture()
def fake_address_id():
    return {
        "dataList": [
            {
                "UniqueId": "dave",
            }
        ],
    }


@pytest.fixture
def client_with_cache(fake_calendar, fake_address_id):
    client = api.Avri("1234AB", 42)
    client._cache = Cache(client._parse_content(fake_calendar), datetime.now())
    return client


def test_parse_content(fake_calendar):
    client = api.Avri("1234AB", 42)
    data = client._parse_content(fake_calendar)
    assert len(data) == 8
    assert len([_ for _ in data if _.name == "GREEN"]) == 2
    assert len([_ for _ in data if _.name == "PAPER"]) == 3
    assert len([_ for _ in data if _.name == "PACKAGES"]) == 3


def test_parse_address(fake_address_id):
    with requests_mock.Mocker() as m:
        m.post(f'{BASE_URL}{FETCH_ADDRESS}', content=json.dumps(fake_address_id).encode())
        client = api.Avri("1234AB", 42)
        assert client.get_address_id() == "dave"


def test_upcoming_new(client_with_cache):
    assert client_with_cache.upcoming(datetime(2021, 1, 21)) == Garbage("GREEN", datetime(2021, 1, 21))


def test_upcoming_today(client_with_cache):
    assert client_with_cache.upcoming(datetime(2021, 2, 9)) == Garbage("PACKAGES", datetime(2021, 2, 9))


def test_upcoming_of_each_new(client_with_cache):
    assert client_with_cache.upcoming_of_each(datetime(2020, 1, 6)) == [
        Garbage("GREEN", datetime(2021, 1, 21)),
        Garbage("PAPER", datetime(2021, 2, 2)),
        Garbage("PACKAGES", datetime(2021, 2, 9)),
    ]


def test_upcoming_of_each_today(client_with_cache):
    assert client_with_cache.upcoming_of_each(datetime(2021, 2, 3)) == [
        Garbage("GREEN", datetime(2021, 2, 4)),
        Garbage("PACKAGES", datetime(2021, 2, 9)),
        Garbage("PAPER", datetime(2021, 3, 2)),
    ]
