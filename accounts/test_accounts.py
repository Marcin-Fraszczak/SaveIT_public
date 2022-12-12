import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

import django
django.setup()


@pytest.fixture
def client():
    client = Client()
    return client

@pytest.fixture
def user():
    user = get_user_model()(username="testuser")
    user.save()
    client.force_login(user)
    return user


@pytest.mark.django_db
def test_url_exists_at_correct_location(client, user):
    response = client.get("/accounts/main/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_url_available_under_specific_name(client, user):
    response = client.get(reverse("accounts:dashboard"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_proper_template_loaded(client, user):
    response = client.get(reverse("accounts:dashboard"))
    # for t in response.templates:
    #     print(t.name)
    assert 'accounts/dashboard.html' in (t.name for t in response.templates)
