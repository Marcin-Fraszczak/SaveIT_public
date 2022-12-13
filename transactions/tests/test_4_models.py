"""
Tests for 4 models: Category, Counterparty, Wallet, SavingsPlan
"""

import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

from transactions import models

name = 'testuser'
items = ["catgory", "counterparty", "wallet", "savings_plan"]
actions = ["add", "list"]


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def user():
    user = get_user_model()(username=name)
    user.save()
    return user


@pytest.fixture
def object(user):
    if item == "savings_plan":
        object = translate(item, 1)(
            name="test",
            initial_value=1000,
            monthly_goal=5000,
            curve_type=1,
            owner=user,
        )
    else:
        object = translate(item, 1)(
            name="test",
            description="desc",
            owner=user,
        )
    return object


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


for item in items:
    @pytest.mark.django_db
    def test_url_exists_at_correct_location(client, user):
        client.force_login(user)
        for action in actions:
            response = client.get(f"/finances/{action}/{item}/")
            assert response.status_code == 200


    @pytest.mark.django_db
    def test_url_available_under_specific_name(client, user):
        client.force_login(user)
        for action in actions:
            response = client.get(reverse(f"transactions:{action}_{item}"))
            assert response.status_code == 200


    def test_access_not_possible_without_login(client):
        for action in actions:
            response = client.get(reverse(f"transactions:{action}_{item}"))
            assert response.url == reverse("login")


    @pytest.mark.django_db
    def test_proper_template_loaded(client, user):
        client.force_login(user)
        response = client.get(reverse(f'transactions:list_{item}'))
        assert f'transactions/list_{item}.html' in (t.name for t in response.templates)
        assert 'partials/_dash_menu.html' in (t.name for t in response.templates)
        assert f"Account: {user.username}" in response.content.decode('UTF-8')
        assert 'Nothing to display' in response.content.decode('UTF-8')


    @pytest.mark.django_db
    def test_item_add_to_db_command(client, user, object):
        client.force_login(user)

        # empty database, should be 0 items
        items_before = translate(item, 0)

        # manually created 1 item
        object.save()

        # should be 1 item in a database
        items_after = translate(item, 0)

        assert items_after - items_before == 1


    @pytest.mark.django_db
    def test_item_add_to_db_form(client, user):
        client.force_login(user)

        # empty database, should be 0 items
        items_before = translate(item, 0)

        # created second item using form
        if item == "savings_plan":
            response = client.post(
                reverse(f'transactions:add_{item}'),
                {
                    "name": f"New {item}",
                    "initial_value": 1000,
                    "monthly_goal": 2000,
                    "curve_type": 1,
                    "owner": user,
                })
        else:
            response = client.post(
                reverse(f'transactions:add_{item}'),
                {
                    "name": f"New {item}",
                    "description": f"new {item}",
                    "owner": user,
                })

        # should be 1 item in a database
        items_after = translate(item, 0)

        last_item = translate(item, 2)

        assert response.status_code == 302
        assert response.url == f"/finances/list/{item}/"
        assert items_after - items_before == 1
        assert last_item.name == f"New {item}".upper()


    @pytest.mark.django_db
    def test_update_view(client, user, object):
        client.force_login(user)
        object.save()
        if item == "savings_plan":
            response = client.post(
                reverse(f'transactions:modify_{item}', args=f"{object.pk}"),
                {
                    "name": f"Update {item}",
                    "initial_value": 2000,
                    "monthly_goal": 4000,
                    "curve_type": 2,
                    "owner": user,
                })
        else:
            response = client.post(
                reverse(f'transactions:modify_{item}', args=f"{object.pk}"),
                {
                    "name": f"Update {item}",
                    "description": f"new {item}",
                    "owner": user,
                })

        modified_item = translate(item, 1).objects.get(pk=object.pk)
        assert response.status_code == 302
        assert modified_item.name == f"Update {item}".upper()


    @pytest.mark.django_db
    def test_delete_view(client, user, object):
        client.force_login(user)
        object.save()
        items_before = translate(item, 0)
        response = client.get(reverse(f'transactions:delete_{item}', args=f"{object.pk}"))
        items_after = translate(item, 0)

        assert response.status_code == 302
        assert items_before - items_after == 1


    @pytest.mark.django_db
    def test_access_denied_for_not_logged_in(client, user, object):
        client.logout()
        object.save()

        commands = [
            client.post(reverse(f'transactions:add_{item}')),
            client.get(reverse(f'transactions:list_{item}')),
            client.post(reverse(f'transactions:modify_{item}', args=f"{object.pk}")),
            client.post(reverse(f'transactions:delete_{item}', args=f"{object.pk}")),
        ]

        for comm in commands:
            response = comm

        # Dopisać testy