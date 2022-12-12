import pytest
from django.test import Client
from django.urls import reverse


import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'


@pytest.fixture
def client():
    client = Client()
    return client


def test_url_exists_at_correct_location(client):
    response = client.get("/")
    assert response.status_code == 200


def test_url_available_under_specific_name(client):
    response = client.get(reverse("home:home"))
    assert response.status_code == 200



