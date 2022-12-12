import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

import django
django.setup()


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


def test_proper_template_loaded(client):
    response = client.get(reverse("home:home"))
    # for t in response.templates:
    #     print(t.name)
    assert 'home/home.html' in (t.name for t in response.templates)


@pytest.mark.django_db
def test_proper_content_loaded(client):
    response = client.get(reverse("home:home"))
    # print(response.content.decode('UTF-8'))
    assert "<strong>Take control</strong>" in response.content.decode('UTF-8')
    user = get_user_model()(username="testuser")
    user.save()
    client.force_login(user)
    response = client.get(reverse("home:home"))
    # print(response.content.decode('UTF-8'))
    assert "<strong>You're in control</strong>" in response.content.decode('UTF-8')
    client.logout()
    response = client.get(reverse("home:home"))
    # print(response.content.decode('UTF-8'))
    assert "<strong>Take control</strong>" in response.content.decode('UTF-8')

