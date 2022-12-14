"""
Tests for 4 models: Category, Counterparty, Wallet, SavingsPlan
"""

import pytest
from django.urls import reverse

from plans.models import SavingsPlan
from wallets.models import Wallet

items = ["wallet", "savings_plan"]


def translate(item, comm):
    translate_dict = {

        # "item": (
        #     0 - "number of items in db",
        #     1 - "model name",
        #     2 - "last item in db",
        #     3 - "app name",
        # ),

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
        item1 = prepare_data[item]
        item2 = prepare_data[f"{item}2"]
        user = prepare_data["user"]
        client.force_login(user)

        response = client.get(f"/{item}/default/{item1.pk}/{item2.pk}/")
        assert response.status_code == 302
        response = client.get(reverse(f"{translate(item, 'app')}:make_default_{item}", args=[f"{item1.pk}", f"{item2.pk}"]))
        assert response.status_code == 302

#
# @pytest.mark.django_db
# def test_update_view(client, prepare_data):
#     for item in items:
#         user = prepare_data["user"]
#         client.force_login(user)
#         obj = prepare_data[item]
#         obj.save()
#
#         if item == "savings_plan":
#             response = client.post(
#                 reverse(f"{translate(item, 'app')}:modify_{item}", args=[f"{obj.pk}"]),
#                 {
#                     "name": f"Update {item}",
#                     "initial_value": 2000,
#                     "monthly_goal": 4000,
#                     "curve_type": 2,
#                     "owner": user,
#                 })
#         else:
#             response = client.post(
#                 reverse(f"{translate(item, 'app')}:modify_{item}", args=[f"{obj.pk}"]),
#                 {
#                     "name": f"Update {item}",
#                     "owner": user,
#                 })
#
#         modified_item = translate(item, "model").objects.get(pk=obj.pk)
#         assert response.status_code == 302
#         assert modified_item.name == f"Update {item}".upper()
#
#
# @pytest.mark.django_db
# def test_delete_view(client, prepare_data):
#     for item in items:
#         user = prepare_data["user"]
#         client.force_login(user)
#         obj = prepare_data[item]
#         obj.save()
#
#         items_before = translate(item, "count")
#         response = client.post(
#             reverse(f"{translate(item, 'app')}:modify_{item}", args=[f"{obj.pk}"]),
#             {"delete": ''})
#         items_after = translate(item, "count")
#
#         assert response.status_code == 302
#         assert items_before - items_after == 1
#
#
# @pytest.mark.django_db
# def test_access_denied_for_not_logged_in(client, prepare_data):
#     for item in items:
#         obj = prepare_data[item]
#         obj.save()
#         client.logout()
#
#         commands = [
#             client.get(reverse(f"{translate(item, 'app')}:add_{item}")),
#             client.get(reverse(f"{translate(item, 'app')}:list_{item}")),
#             client.get(reverse(f"{translate(item, 'app')}:modify_{item}", args=[f"{obj.pk}"])),
#
#             client.post(reverse(f"{translate(item, 'app')}:add_{item}")),
#             client.post(reverse(f"{translate(item, 'app')}:modify_{item}", args=[f"{obj.pk}"])),
#             client.post(reverse(f"{translate(item, 'app')}:modify_{item}", args=[f"{obj.pk}"]), {'delete': ''}),
#         ]
#         for comm in commands:
#             response = comm
#
#             assert response.status_code == 302
#             assert reverse("login") in response.url
