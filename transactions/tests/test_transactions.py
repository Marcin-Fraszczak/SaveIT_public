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
item = "transaction"
actions = ["add", "list"]


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
        assert response.url == reverse('login')


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


# Nie działa dodawanie obiektu przez formularz!!!
@pytest.mark.django_db
def test_adding_new_transaction(client):
    user = get_user_model()(username=name)
    user.save()
    client.force_login(user)
    items_before = models.Transaction.objects.all().count()

    cat = models.Category(
        name="test_cat".upper(),
        description="desc",
        owner=user,
    )
    cat.save()

    cntp = models.Counterparty(
        name="test_cntp".upper(),
        description="desc",
        owner=user,
    )
    cntp.save()

    wallet = Wallet(
        name="test_wallet".upper(),
        description="desc",
        owner=user,
    )
    wallet.save()

    # t1 = models.Transaction(
    #         date=datetime.today().date(),
    #         value="997",
    #         is_profit=True,
    #         notes="test_note",
    #         category=cat,
    #         counterparty=cntp,
    #         owner=user,
    #         )
    # t1.save()
    #
    # t2 = models.Transaction(
    #     date=datetime.today().date(),
    #     value="998",
    #     is_profit=True,
    #     notes="test_note",
    #     category=cat,
    #     counterparty=cntp,
    #     owner=user,
    # )
    # t2.save()

    # to nie chce działać
    response = client.post(
        reverse(f'transactions:add_{item}'),
        {
            # "date": datetime.today().date(),
            "date": "2022-10-10",
            "value": "997",
            "is_profit": 1,
            "notes": "test_note",
            "category": cat.pk,
            "counterparty": cntp.pk,
            "owner": user.pk,
            "wallet": [wallet.pk],
        })

    items_after = models.Transaction.objects.all().count()

    assert response.status_code == 302
    assert response.url == "/finances/list/transaction/"
    assert items_after - items_before == 1

