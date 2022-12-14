import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
from transactions.models import Transaction
from categories.models import Category
from counterparties.models import Counterparty
from wallets.models import Wallet


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def user():
    user = get_user_model()(username=name)
    user.save()
    return user


name = 'testuser'
item = "transaction"
actions = ["add", "list"]


@pytest.mark.django_db
def test_url_exists_at_correct_location(client, user):
    client.force_login(user)
    for action in actions:

        response = client.get(f"/{item}/{action}/")
        assert response.status_code == 200

        response = client.get(reverse(f"transactions:{action}_{item}"))
        assert response.status_code == 200


@pytest.mark.django_db
def test_access_not_possible_without_login(client):
    client.logout()
    for action in actions:
        response = client.get(reverse(f"transactions:{action}_{item}"))
        assert reverse('login') in response.url


@pytest.mark.django_db
def test_proper_template_loaded(client, user):
    client.force_login(user)
    response = client.get(reverse(f'transactions:list_{item}'))

    assert f'transactions/list_{item}.html' in (t.name for t in response.templates)
    assert 'partials/_dash_menu.html' in (t.name for t in response.templates)
    assert f"Account: {user.username}" in response.content.decode('UTF-8')
    assert 'Nothing to display' in response.content.decode('UTF-8')


@pytest.mark.django_db
def test_adding_new_transaction(client, user):
    client.force_login(user)
    items_before = Transaction.objects.all().count()

    cat = Category(
        name="test_cat".upper(),
        owner=user,
    )
    cat.save()

    cntp = Counterparty(
        name="test_cntp".upper(),
        owner=user,
    )
    cntp.save()

    wallet = Wallet(
        name="test_wallet".upper(),
        owner=user,
    )
    wallet.save()

    response = client.post(
        reverse(f'transactions:add_{item}'),
        {
            "date": "2022-10-10",
            "value": "997",
            "is_profit": 1,
            "notes": "test_note",
            "category": cat.pk,
            "counterparty": cntp.pk,
            "owner": user.pk,
            "wallet": [wallet.pk],
        })

    items_after = Transaction.objects.all().count()

    assert response.status_code == 302
    assert response.url == reverse("transactions:list_transaction")
    assert items_after - items_before == 1

