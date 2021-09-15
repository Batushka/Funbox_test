import os
import sys

import pytest
from rest_framework.test import APIClient

sys.path.append(os.path.dirname(__file__))


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def links_data():
    return {
        "links": [
            "https://ya.ru",
            "https://ya.ru?q=123",
            "funbox.ru",
            "https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor",
            "http://gitnub.com/Batushka",
            "netflix.com/ru/"
        ]
    }


