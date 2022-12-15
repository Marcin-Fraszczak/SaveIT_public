"""
Tests for 2 models: Wallet, SavingsPlan. 'Make default' functionality.
"""

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

item = "wallet"


@pytest.mark.django_db
def test_url_exists_at_correct_location(client, prepare_data, translate):
    obj1 = prepare_data[item]
    obj2 = prepare_data[f"{item}2"]
    user = prepare_data["user"]
    client.force_login(user)

    response = client.get(f"/{item}/transfer/{obj1.pk}/{obj2.pk}/")
    assert response.status_code == 302
    assert response.url == reverse(f"{translate[item]['app']}:list_{item}")

    response = client.get(reverse(f"{translate[item]['app']}:transfer_{item}", args=[f"{obj1.pk}", f"{obj2.pk}"]))
    assert response.status_code == 302
    assert response.url == reverse(f"{translate[item]['app']}:list_{item}")

    response = client.get(f"/{item}/transfer/{obj1.pk}/0/")
    assert response.status_code == 200

    response = client.get(reverse(f"{translate[item]['app']}:transfer_{item}", args=[f"{obj1.pk}", "0"]))
    assert response.status_code == 200



@pytest.mark.django_db
def test_correct_template_loaded(client, prepare_data, translate):
    obj1 = prepare_data[item]
    user = prepare_data["user"]
    client.force_login(user)

    response = client.get(reverse(f"{translate[item]['app']}:transfer_{item}", args=[f"{obj1.pk}", "0"]))
    assert f"transactions/transfer_{item}.html" in (t.name for t in response.templates)
    assert 'partials/_dash_menu.html' in (t.name for t in response.templates)
    assert f"Account: {user.username}" in response.content.decode('UTF-8')


@pytest.mark.django_db
def test_transfer_transaction(client, prepare_data, translate):
    obj1 = prepare_data[item]
    obj2 = prepare_data[f"{item}2"]
    transaction = prepare_data["transaction"]
    transaction.wallet.add(obj1)

    user = prepare_data["user"]
    client.force_login(user)

    assert len(obj1.wlt_transaction.all()) == 1
    assert len(obj2.wlt_transaction.all()) == 0

    response = client.get(reverse(f"{translate[item]['app']}:transfer_{item}", args=[f"{obj1.pk}", f"{obj2.pk}"]))

    assert len(obj1.wlt_transaction.all()) == 0
    assert len(obj2.wlt_transaction.all()) == 1


@pytest.mark.django_db
def test_access_denied_for_not_logged_in(client, prepare_data, translate):
    obj1 = prepare_data[item]
    obj2 = prepare_data[f"{item}2"]
    transaction = prepare_data["transaction"]
    transaction.wallet.add(obj1)
    client.logout()

    assert len(obj1.wlt_transaction.all()) == 1
    assert len(obj2.wlt_transaction.all()) == 0

    response = client.get(reverse(f"{translate[item]['app']}:transfer_{item}", args=[f"{obj1.pk}", f"{obj2.pk}"]))
    assert response.status_code == 302
    assert reverse('login') in response.url
    assert len(obj1.wlt_transaction.all()) == 1
    assert len(obj2.wlt_transaction.all()) == 0

    response = client.get(reverse(f"{translate[item]['app']}:transfer_{item}", args=[f"{obj1.pk}", "0"]))
    assert response.status_code == 302
    assert reverse('login') in response.url


@pytest.mark.django_db
def test_access_denied_for_different_user(client, prepare_data, translate):
    client.logout()
    obj1 = prepare_data[item]
    obj2 = prepare_data[f"{item}2"]
    transaction = prepare_data["transaction"]
    transaction.wallet.add(obj1)

    user = get_user_model()(username="intruder")
    user.save()
    client.force_login(user)

    assert len(obj1.wlt_transaction.all()) == 1
    assert len(obj2.wlt_transaction.all()) == 0

    response = client.get(reverse(f"{translate[item]['app']}:transfer_{item}", args=[f"{obj1.pk}", f"{obj2.pk}"]))
    assert response.status_code == 404
    assert len(obj1.wlt_transaction.all()) == 1
    assert len(obj2.wlt_transaction.all()) == 0
