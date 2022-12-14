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


def translate(item, comm):
    translate_dict = {

        # "item": (
        #     0 - "number of items in db",
        #     1 - "model name",
        #     2 - "last item in db",
        #     3 - "app name",
        # ),

        "category": {
            "count": Category.objects.all().count(),
            "model": Category,
            "last": Category.objects.last(),
            "app": "categories",
        },
        "counterparty": {
            "count": Counterparty.objects.all().count(),
            "model": Counterparty,
            "last": Counterparty.objects.last(),
            "app": "counterparties",
        },
        "wallet": {
            "count": Wallet.objects.all().count(),
            "model": Wallet,
            "last": Wallet.objects.last(),
            "app": "wallets",
        },
        "savings_plan": {
            "count": SavingsPlan.objects.all().count(),
            "model": SavingsPlan,
            "last": SavingsPlan.objects.last(),
            "app": "plans",
        },
    }
    return translate_dict[item][comm]


@pytest.mark.django_db
def test_url_exists_at_correct_location(client, prepare_data):
    for item in items:
        pk = prepare_data[item].pk
        user = prepare_data["user"]
        client.force_login(user)

        for action in ["add", "list"]:
            response = client.get(f"/{item}/{action}/")
            assert response.status_code == 200
            response = client.get(reverse(f"{translate(item, 'app')}:{action}_{item}"))
            assert response.status_code == 200
        response = client.get(f"/{item}/modify/{pk}/")
        assert response.status_code == 200
        response = client.get(reverse(f"{translate(item, 'app')}:modify_{item}", args=f"{pk}"))
        assert response.status_code == 200


@pytest.mark.django_db
def test_proper_template_loaded(client, user):
    for item in items:
        client.force_login(user)
        response = client.get(reverse(f"{translate(item, 'app')}:list_{item}"))
        assert f'transactions/list_{item}.html' in (t.name for t in response.templates)
        assert 'partials/_dash_menu.html' in (t.name for t in response.templates)
        assert f"Account: {user.username}" in response.content.decode('UTF-8')
        assert 'Nothing to display' in response.content.decode('UTF-8')


@pytest.mark.django_db
def test_item_add_to_db_form(client, user):
    for item in items:
        client.force_login(user)

        items_before = translate(item, "count")

        if item == "savings_plan":
            response = client.post(
                reverse(f"{translate(item, 'app')}:add_{item}"),
                {
                    "name": f"New {item}",
                    "initial_value": 1000,
                    "monthly_goal": 2000,
                    "curve_type": 1,
                    "owner": user,
                })
        else:
            response = client.post(
                reverse(f"{translate(item, 'app')}:add_{item}"),
                {
                    "name": f"New {item}",
                    "owner": user,
                })

        items_after = translate(item, "count")

        last_item = translate(item, "last")

        assert response.status_code == 302
        assert response.url == reverse(f"{translate(item, 'app')}:list_{item}")
        assert items_after - items_before == 1
        assert last_item.name == f"New {item}".upper()


@pytest.mark.django_db
def test_update_view(client, prepare_data):
    for item in items:
        user = prepare_data["user"]
        client.force_login(user)
        obj = prepare_data[item]
        obj.save()

        if item == "savings_plan":
            response = client.post(
                reverse(f"{translate(item, 'app')}:modify_{item}", args=f"{obj.pk}"),
                {
                    "name": f"Update {item}",
                    "initial_value": 2000,
                    "monthly_goal": 4000,
                    "curve_type": 2,
                    "owner": user,
                })
        else:
            response = client.post(
                reverse(f"{translate(item, 'app')}:modify_{item}", args=f"{obj.pk}"),
                {
                    "name": f"Update {item}",
                    "owner": user,
                })

        modified_item = translate(item, "model").objects.get(pk=obj.pk)
        assert response.status_code == 302
        assert modified_item.name == f"Update {item}".upper()


@pytest.mark.django_db
def test_delete_view(client, prepare_data):
    for item in items:
        user = prepare_data["user"]
        client.force_login(user)
        obj = prepare_data[item]
        obj.save()

        items_before = translate(item, "count")
        response = client.post(
            reverse(f"{translate(item, 'app')}:modify_{item}", args=f"{obj.pk}"),
            {"delete": ''})
        items_after = translate(item, "count")

        assert response.status_code == 302
        assert items_before - items_after == 1


@pytest.mark.django_db
def test_access_denied_for_not_logged_in(client, prepare_data):
    for item in items:
        obj = prepare_data[item]
        obj.save()
        client.logout()

        commands = [
            client.get(reverse(f"{translate(item, 'app')}:add_{item}")),
            client.get(reverse(f"{translate(item, 'app')}:list_{item}")),
            client.get(reverse(f"{translate(item, 'app')}:modify_{item}", args=f"{obj.pk}")),

            client.post(reverse(f"{translate(item, 'app')}:add_{item}")),
            client.post(reverse(f"{translate(item, 'app')}:modify_{item}", args=f"{obj.pk}")),
            client.post(reverse(f"{translate(item, 'app')}:modify_{item}", args=f"{obj.pk}"), {'delete': ''}),
        ]
        for comm in commands:
            response = comm

            assert response.status_code == 302
            assert reverse("login") in response.url
