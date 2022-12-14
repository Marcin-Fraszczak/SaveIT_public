import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse


def test_url_exists_at_correct_location(client):
    response = client.get("/")
    assert response.status_code == 200
    response = client.get(reverse("home:home"))
    assert response.status_code == 200


def test_proper_template_loaded(client):
    response = client.get(reverse("home:home"))
    assert 'home/home.html' in (t.name for t in response.templates)
    assert 'partials/_menu.html' in (t.name for t in response.templates)
    assert 'partials/_footer.html' in (t.name for t in response.templates)
    assert '_base_.html' in (t.name for t in response.templates)


@pytest.mark.django_db
def test_proper_content_loaded(client, user):
    response = client.get(reverse("home:home"))
    assert "<strong>Take control</strong>" in response.content.decode('UTF-8')

    client.force_login(user)
    response = client.get(reverse("home:home"))
    assert "<strong>You're in control</strong>" in response.content.decode('UTF-8')

    client.logout()
    response = client.get(reverse("home:home"))
    assert "<strong>Take control</strong>" in response.content.decode('UTF-8')

