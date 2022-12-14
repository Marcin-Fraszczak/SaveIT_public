"""
Tests for 4 models: Category, Counterparty, Wallet, SavingsPlan
"""

import pytest
from django.urls import reverse

from categories.models import Category
from counterparties.models import Counterparty
from plans.models import SavingsPlan
from transactions.models import Transaction
from wallets.models import Wallet

items = ["category", "counterparty", "wallet", "savings_plan"]
actions = ["add", "list"]


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
            owner=user,
        )
    return object


def translate(item, ind):
    translate_dict = {
        "category": (
            Category.objects.all().count(),
            Category,
            Category.objects.last(),
            "categories",
        ),
        "counterparty": (
            Counterparty.objects.all().count(),
            Counterparty,
            Counterparty.objects.last(),
            "counterparties,"
        ),
        "wallet": (
            Wallet.objects.all().count(),
            Wallet,
            Wallet.objects.last(),
            "wallets",
        ),
        "savings_plan": (
            SavingsPlan.objects.all().count(),
            SavingsPlan,
            SavingsPlan.objects.last(),
            "plans",
        ),
    }
    return translate_dict[item][ind]


for item in items:
    @pytest.mark.django_db
    def test_url_exists_at_correct_location(client, user):
        client.force_login(user)
        for action in actions:
            response = client.get(f"/{item}/{action}/")
            assert response.status_code == 200
            response = client.get(reverse(f"{translate(item, 3)}:{action}_{item}"))
            assert response.status_code == 200


    @pytest.mark.django_db
    def test_access_not_possible_without_login(client):
        client.logout()
        for action in actions:
            response = client.get(reverse(f"{translate(item, 3)}:{action}_{item}"))
            assert reverse("login") in response.url


    @pytest.mark.django_db
    def test_proper_template_loaded(client, user):
        client.force_login(user)
        response = client.get(reverse(f'{translate(item, 3)}:list_{item}'))
        assert f'transactions/list_{item}.html' in (t.name for t in response.templates)
        assert 'partials/_dash_menu.html' in (t.name for t in response.templates)
        assert f"Account: {user.username}" in response.content.decode('UTF-8')
        assert 'Nothing to display' in response.content.decode('UTF-8')


    @pytest.mark.django_db
    def test_item_add_to_db_form(client, user):
        client.force_login(user)

        items_before = translate(item, 0)

        if item == "savings_plan":
            response = client.post(
                reverse(f'{translate(item, 3)}:add_{item}'),
                {
                    "name": f"New {item}",
                    "initial_value": 1000,
                    "monthly_goal": 2000,
                    "curve_type": 1,
                    "owner": user,
                })
        else:
            response = client.post(
                reverse(f'{translate(item, 3)}:add_{item}'),
                {
                    "name": f"New {item}",
                    "owner": user,
                })

        items_after = translate(item, 0)

        last_item = translate(item, 2)

        assert response.status_code == 302
        assert response.url == reverse(f'{translate(item, 3)}:list_{item}')
        assert items_after - items_before == 1
        assert last_item.name == f"New {item}".upper()


    @pytest.mark.django_db
    def test_update_view(client, user, object):
        client.force_login(user)
        object.save()
        if item == "savings_plan":
            response = client.post(
                reverse(f'{translate(item, 3)}:modify_{item}', args=f"{object.pk}"),
                {
                    "name": f"Update {item}",
                    "initial_value": 2000,
                    "monthly_goal": 4000,
                    "curve_type": 2,
                    "owner": user,
                })
        else:
            response = client.post(
                reverse(f'{translate(item, 3)}:modify_{item}', args=f"{object.pk}"),
                {
                    "name": f"Update {item}",
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
        response = client.get(reverse(f'{translate(item, 3)}:delete_{item}', args=f"{object.pk}"))
        items_after = translate(item, 0)

        assert response.status_code == 302
        assert items_before - items_after == 1


    @pytest.mark.django_db
    def test_access_denied_for_not_logged_in(client, user, object):
        client.logout()
        object.save()

        commands = [
            client.post(reverse(f'{translate(item, 3)}:add_{item}')),
            client.get(reverse(f'{translate(item, 3)}:list_{item}')),
            client.post(reverse(f'{translate(item, 3)}:modify_{item}', args=f"{object.pk}")),
            client.post(reverse(f'{translate(item, 3)}:delete_{item}', args=f"{object.pk}")),
        ]

        for comm in commands:
            response = comm

            assert response.status_code == 302
            assert reverse("login") in response.url
