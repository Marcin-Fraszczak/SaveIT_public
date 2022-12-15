"""
Tests for 4 models: Category, Counterparty, Wallet, SavingsPlan
"""

import pytest
from django.urls import reverse

items = ["category", "counterparty", "wallet", "savings_plan"]


@pytest.mark.django_db
def test_url_exists_at_correct_location(client, prepare_data, translate):
    for item in items:
        pk = prepare_data[item].pk
        user = prepare_data["user"]
        client.force_login(user)

        for action in ["add", "list"]:
            response = client.get(f"/{item}/{action}/")
            assert response.status_code == 200
            response = client.get(reverse(f"{translate[item]['app']}:{action}_{item}"))
            assert response.status_code == 200
        response = client.get(f"/{item}/modify/{pk}/")
        assert response.status_code == 200
        response = client.get(reverse(f"{translate[item]['app']}:modify_{item}", args=[f"{pk}"]))
        assert response.status_code == 200


@pytest.mark.django_db
def test_proper_template_loaded(client, user, translate):
    for item in items:
        client.force_login(user)
        response = client.get(reverse(f"{translate[item]['app']}:list_{item}"))
        assert f'transactions/list_{item}.html' in (t.name for t in response.templates)
        assert 'partials/_dash_menu.html' in (t.name for t in response.templates)
        assert f"Account: {user.username}" in response.content.decode('UTF-8')
        assert 'Nothing to display' in response.content.decode('UTF-8')


@pytest.mark.django_db
def test_item_add_to_db_form(client, user, translate):
    for item in items:
        client.force_login(user)

        items_before = translate[item]['model'].objects.all().count()

        if item == "savings_plan":
            response = client.post(
                reverse(f"{translate[item]['app']}:add_{item}"),
                {
                    "name": f"New {item}",
                    "initial_value": 1000,
                    "monthly_goal": 2000,
                    "curve_type": 1,
                })
        else:
            response = client.post(
                reverse(f"{translate[item]['app']}:add_{item}"),
                {
                    "name": f"New {item}",
                })

        items_after = translate[item]['model'].objects.all().count()

        last_item = translate[item]['model'].objects.last()

        assert response.status_code == 302
        assert response.url == reverse(f"{translate[item]['app']}:list_{item}")
        assert last_item.name == f"New {item}".upper()
        assert items_after - items_before == 1


@pytest.mark.django_db
def test_update_view(client, prepare_data, translate):
    for item in items:
        user = prepare_data["user"]
        client.force_login(user)
        obj = prepare_data[item]

        if item == "savings_plan":
            response = client.post(
                reverse(f"{translate[item]['app']}:modify_{item}", args=[f"{obj.pk}"]),
                {
                    "name": f"Update {item}",
                    "initial_value": 2000,
                    "monthly_goal": 4000,
                    "curve_type": 2,
                    "owner": user,
                })
        else:
            response = client.post(
                reverse(f"{translate[item]['app']}:modify_{item}", args=[f"{obj.pk}"]),
                {
                    "name": f"Update {item}",
                    "owner": user,
                })

        modified_item = translate[item]['model'].objects.get(pk=obj.pk)
        assert response.status_code == 302
        assert modified_item.name == f"Update {item}".upper()


@pytest.mark.django_db
def test_delete_item(client, prepare_data, translate):
    for item in items:
        user = prepare_data["user"]
        client.force_login(user)
        obj = prepare_data[item]

        items_before = translate[item]['model'].objects.all().count()

        response = client.post(
            reverse(f"{translate[item]['app']}:modify_{item}", args=[f"{obj.pk}"]),
            {"delete": ''}
        )

        items_after = translate[item]['model'].objects.all().count()

        assert response.status_code == 302
        assert items_before - items_after == 1


@pytest.mark.django_db
def test_access_denied_for_not_logged_in(client, prepare_data, translate):
    for item in items:
        obj = prepare_data[item]
        client.logout()

        commands = [
            client.get(reverse(f"{translate[item]['app']}:add_{item}")),
            client.get(reverse(f"{translate[item]['app']}:list_{item}")),
            client.get(reverse(f"{translate[item]['app']}:modify_{item}", args=[f"{obj.pk}"])),

            client.post(reverse(f"{translate[item]['app']}:add_{item}")),
            client.post(reverse(f"{translate[item]['app']}:modify_{item}", args=[f"{obj.pk}"])),
            client.post(reverse(f"{translate[item]['app']}:modify_{item}", args=[f"{obj.pk}"]), {'delete': ''}),
        ]
        for comm in commands:
            response = comm

            assert response.status_code == 302
            assert reverse("login") in response.url


