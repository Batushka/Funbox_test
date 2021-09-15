import pytest

from datetime import datetime
import math

import requests
from django.urls import reverse


def test_visited_links(api_client, links_data):
    url = 'http://127.0.0.1:8000/checker/visited-links/'
    response = requests.post(url, json=links_data)
    assert response.status_code == 201, response.json()
    response = requests.put(url, json=links_data)
    assert response.status_code == 405, response.json()
    response = requests.delete(url, json=links_data)
    assert response.status_code == 405, response.json()


@pytest.mark.parametrize(
    'from_, to, status_code', [
        (math.trunc(datetime.timestamp(datetime.now()) - 30),
         math.trunc(datetime.timestamp(datetime.now()) + 30),
         200
         ),
        (math.trunc(datetime.timestamp(datetime.now()) + 30),
         math.trunc(datetime.timestamp(datetime.now()) + 90),
         404
         ),
        (math.trunc(datetime.timestamp(datetime.now()) - 90),
         math.trunc(datetime.timestamp(datetime.now()) - 30),
         404
         ),
    ]
)
def test_visited_domains(api_client, from_, to, status_code):
    query_filters = {'from': from_, 'to': to}
    url = 'http://127.0.0.1:8000/checker/visited-domains/'
    response = requests.get(url, params=query_filters)
    assert response.status_code == status_code, response.json()


def test_visited_domains_other_http_methods(api_client):
    from_ = math.trunc(datetime.timestamp(datetime.now()) - 30)
    to = math.trunc(datetime.timestamp(datetime.now()) + 30)
    url = 'http://127.0.0.1:8000/checker/visited-domains/'
    query_filters = {'from': from_, 'to': to}
    response = requests.post(url, json=query_filters)
    assert response.status_code == 405, response.json()
    response = requests.put(url, data=query_filters)
    assert response.status_code == 405, response.json()
    response = requests.delete(url)
    assert response.status_code == 405, response.json()


@pytest.mark.parametrize(
    'from_, to, status_code', [
        ('163158str0', '1631637415', 400),
        ('1631580100', '163163str5', 400),
        ('163158010', '1631637415', 400),
        ('1631580100', '163163741', 400),
        ('16315801002', '1631637415', 400),
        ('1631580100', '16316374152', 400),
    ]
)
def test_visited_domains_not_integer_filters(api_client, from_,
                                             to, status_code):
    query_filters = {'from': from_, 'to': to}
    url = 'http://127.0.0.1:8000/checker/visited-domains/'
    response = requests.get(url, params=query_filters)
    assert response.status_code == status_code, response.json()
