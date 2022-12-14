import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse


@pytest.mark.django_db
def test_url_exists_at_correct_location(client, user):
    client.force_login(user)

    response = client.get("/accounts/main/")
    assert response.status_code == 200
    response = client.get(reverse("accounts:dashboard"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_access_not_possible_without_login(client):
    client.logout()
    response = client.get(reverse("accounts:dashboard"))
    assert reverse("login") in response.url


@pytest.mark.django_db
def test_proper_template_loaded(client, user):
    client.force_login(user)
    response = client.get(reverse("accounts:dashboard"))

    assert 'accounts/dashboard.html' in (t.name for t in response.templates)
    assert 'partials/_dash_menu.html' in (t.name for t in response.templates)
    assert f"Account: {user.username}" in response.content.decode('UTF-8')


@pytest.mark.django_db
def test_user_sign_up_and_log_in(client):
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

    response = client.post(
        reverse("login"),
        {
            "username": "testuser",
            "password": "Testpass123",
        }
    )

    assert response.status_code == 302
    assert response.url == reverse("accounts:dashboard")


@pytest.mark.django_db
def test_login_impossible_with_wrong_data(client):
    response = client.post(
        reverse("login"),
        {
            "username": "YabaDabaDoo",
            "password": "Random123Password",
        }
    )

    assert response.status_code == 200
    assert not response.context["user"].is_authenticated
