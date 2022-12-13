from datetime import datetime

import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

import django
django.setup()

from transactions import models


@pytest.fixture
def client():
    client = Client()
    return client


name = 'testuser'
item = "wallet"
actions = ["add", "list"]


def translate(item, ind):
    translate_dict = {
        "category": (
            models.Category.objects.all().count(),
            models.Category,
            models.Category.objects.last()
        ),
        "counterparty": (
            models.Counterparty.objects.all().count(),
            models.Counterparty,
            models.Counterparty.objects.last()
        ),
        "wallet": (
            models.Wallet.objects.all().count(),
            models.Wallet,
            models.Wallet.objects.last()
        ),
        "savings_plan": (
            models.SavingsPlan.objects.all().count(),
            models.SavingsPlan,
            models.SavingsPlan.objects.last()
        ),
    }
    return translate_dict[item][ind]


@pytest.mark.django_db
def test_url_exists_at_correct_location(client):
    user = get_user_model()(username=name)
    user.save()
    client.force_login(user)
    for action in actions:
        response = client.get(f"/finances/{action}/{item}/")
        assert response.status_code == 200


@pytest.mark.django_db
def test_url_available_under_specific_name(client):
    user = get_user_model()(username=name)
    user.save()
    client.force_login(user)
    for action in actions:
        response = client.get(reverse(f"transactions:{action}_{item}"))
        assert response.status_code == 200


def test_access_not_possible_without_login(client):
    for action in actions:
        response = client.get(reverse(f"transactions:{action}_{item}"))
        assert response.url == reverse("login")

#
@pytest.mark.django_db
def test_proper_template_loaded(client):
    user = get_user_model()(username=name)
    user.save()
    client.force_login(user)
    response = client.get(reverse(f'transactions:list_{item}'))
    assert f'transactions/list_{item}.html' in (t.name for t in response.templates)
    assert 'partials/_dash_menu.html' in (t.name for t in response.templates)
    assert f"Account: {user.username}" in response.content.decode('UTF-8')
    assert 'Nothing to display' in response.content.decode('UTF-8')


@pytest.mark.django_db
def test_category_manipulation(client):
    user = get_user_model()(username=name)
    user.save()
    client.force_login(user)

    # empty database, should be 0 items
    items_before = translate(item, 0)

    # manually created 1 item
    o = translate(item, 1)(
        name="test",
        description="desc",
        owner=user,
    )
    o.save()

    # should be 1 item in a database
    items_manual = translate(item, 0)

    # created second item using form
    response = client.post(
        reverse(f'transactions:add_{item}'),
        {
            "name": f"New {item}",
            "description": f"new {item}",
            "owner": user,
        })

    # should be 2 items
    items_form = translate(item, 0)

    assert response.status_code == 302
    assert response.url == f"/finances/list/{item}/"
    assert items_manual - items_before == 1
    assert items_form - items_manual == 1

    # for update view
    pk = translate(item, 2).pk
    response = client.post(
        reverse(f'transactions:modify_{item}', args=f"{pk}"),
        {
            "name": f"Updated {item}",
            "description": f"Updated {item}",
        })

    # assert response.status_code == 302
    assert translate(item, 2).name == f"Updated {item}".upper()
    assert translate(item, 2).description == f"Updated {item}"

    # for delete view
    items_before = translate(item, 0)
    response = client.get(reverse(f'transactions:delete_{item}', args=f"{translate(item, 2).pk}"))
    items_after = translate(item, 0)
    # assert response.status_code == 302
    assert items_before - items_after == 1

    # user not logged in
    client.logout()
    items_before = translate(item, 0)
    response = client.get(reverse(f'transactions:delete_{item}', args=f"{translate(item, 0)}"))
    items_after = translate(item, 0)
    assert response.status_code == 302
    assert response.url == reverse("login")
    assert items_before == items_after
