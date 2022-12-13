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


# @pytest.fixture
# def user():
#     user = get_user_model()(username="testuser")
#     user.save()
#     client.force_login(user)
#     return user


@pytest.mark.django_db
def test_url_exists_at_correct_location(client):
    user = get_user_model()(username="testuser")
    user.save()
    client.force_login(user)
    response = client.get("/accounts/main/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_url_available_under_specific_name(client):
    user = get_user_model()(username="testuser")
    user.save()
    client.force_login(user)
    response = client.get(reverse("accounts:dashboard"))
    assert response.status_code == 200


def test_access_not_possible_without_login(client):
    response = client.get(reverse("accounts:dashboard"))
    assert response.url == reverse("login")


@pytest.mark.django_db
def test_proper_template_loaded(client):
    user = get_user_model()(username="testuser")
    user.save()
    client.force_login(user)
    response = client.get(reverse("accounts:dashboard"))
    assert 'accounts/dashboard.html' in (t.name for t in response.templates)
    assert 'partials/_dash_menu.html' in (t.name for t in response.templates)
    assert f"Account: {user.username}" in response.content.decode('UTF-8')


@pytest.mark.django_db
def test_user_manipulation(client):

    # user creation via form
    users_before = get_user_model().objects.all().count()
    response = client.post(
        reverse("accounts:register"),
        {
            "username": "testuser",
            "email": "a@a.pl",
            "password1": "Testpass123",
            "password2": "Testpass123",
        }
    )

    users_after = get_user_model().objects.all().count()
    assert response.status_code == 302
    assert response.url == reverse("login")
    assert users_after - users_before == 1

    #  logging in newly created user via form
    response = client.post(
        reverse("login"),
        {
            "username": "testuser",
            "password": "Testpass123",
        }
    )

    assert response.status_code == 302
    assert response.url == reverse("accounts:dashboard")

    # logging out
    response = client.post(reverse("logout"))
    assert response.status_code == 302
    assert response.url == reverse("home:home")

    # logging in with wrong input
    response = client.post(
        reverse("login"),
        {
            "username": "YabaDabaDoo",
            "password": "jneje123REFVV",
        }
    )

    assert response.status_code == 200
    assert not response.context["user"].is_authenticated
