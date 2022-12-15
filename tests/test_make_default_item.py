"""
Tests for 2 models: Wallet, SavingsPlan. 'Make default' functionality.
"""

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

items = ["wallet", "savings_plan"]


@pytest.mark.django_db
def test_url_exists_at_correct_location(client, prepare_data, translate):
    for item in items:
        obj = prepare_data[item]
        user = prepare_data["user"]
        client.force_login(user)

        response = client.get(f"/{item}/default/{obj.pk}/")
        assert response.status_code == 302
        response = client.get(reverse(f"{translate[item]['app']}:make_default_{item}", args=[f"{obj.pk}"]))
        assert response.status_code == 302


@pytest.mark.django_db
def test_change_default_item(client, prepare_data, translate):
    for item in items:

        user = prepare_data["user"]
        client.force_login(user)

        item1 = prepare_data[item]
        item1.is_default = True
        item1.save()
        item2 = prepare_data[f"{item}2"]

        assert item1.is_default is True
        assert item2.is_default is False

        response = client.get(
            reverse(f"{translate[item]['app']}:make_default_{item}", args=[f"{item2.pk}"]))

        item1 = translate[item]["model"].objects.get(pk=item1.pk)
        item2 = translate[item]["model"].objects.get(pk=item2.pk)

        assert response.status_code == 302
        assert response.url == reverse(f"{translate[item]['app']}:list_{item}")
        assert item1.is_default is False
        assert item2.is_default is True



@pytest.mark.django_db
def test_access_denied_for_not_logged_in(client, prepare_data, translate):
    for item in items:

        item1 = prepare_data[item]
        item1.is_default = True
        item1.save()
        item2 = prepare_data[f"{item}2"]

        assert item1.is_default is True
        assert item2.is_default is False

        client.logout()

        response = client.get(
            reverse(f"{translate[item]['app']}:make_default_{item}", args=[f"{item2.pk}"]))

        item1 = translate[item]["model"].objects.get(pk=item1.pk)
        item2 = translate[item]["model"].objects.get(pk=item2.pk)

        assert response.status_code == 302
        assert reverse('login') in response.url
        assert item1.is_default is True
        assert item2.is_default is False


@pytest.mark.django_db
def test_change_default_item_not_possible_for_different_user(client, prepare_data, translate):
    for item in items:
        client.logout()
        user = get_user_model()(username="intruder")
        user.save()
        client.force_login(user)

        item1 = prepare_data[item]
        item1.is_default = True
        item1.save()
        item2 = prepare_data[f"{item}2"]

        assert item1.is_default is True
        assert item2.is_default is False

        response = client.get(
            reverse(f"{translate[item]['app']}:make_default_{item}", args=[f"{item2.pk}"]))

        item1 = translate[item]["model"].objects.get(pk=item1.pk)
        item2 = translate[item]["model"].objects.get(pk=item2.pk)

        assert response.status_code == 302
        assert response.url == reverse(f"{translate[item]['app']}:list_{item}")
        assert item1.is_default is True
        assert item2.is_default is False

        user.delete()
