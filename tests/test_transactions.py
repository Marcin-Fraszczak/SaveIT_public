import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from transactions.models import Transaction

t_item = "transaction"
app_name = "transactions"


@pytest.mark.django_db
def test_url_exists_at_correct_location(client, prepare_data):
    pk = prepare_data[t_item].pk
    client.force_login(prepare_data["user"])

    for action in ["add", "list"]:
        response = client.get(f"/{t_item}/{action}/")
        assert response.status_code == 200
        response = client.get(reverse(f"{app_name}:{action}_{t_item}"))
        assert response.status_code == 200

    response = client.get(f"/{t_item}/modify/{pk}/")
    assert response.status_code == 200
    response = client.get(reverse(f"{app_name}:modify_{t_item}", args=f"{pk}"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_proper_template_loaded(client, prepare_data):
    pk = prepare_data[t_item].pk
    user = prepare_data["user"]
    client.force_login(user)

    for action in ["add", "list"]:
        response = client.get(reverse(f'{app_name}:{action}_{t_item}'))
        assert f'transactions/{action}_{t_item}.html' in (t.name for t in response.templates)
        assert 'partials/_dash_menu.html' in (t.name for t in response.templates)
        assert f"Account: {user.username}" in response.content.decode('UTF-8')

    response = client.get(reverse(f'{app_name}:modify_{t_item}', args=f"{pk}"))
    assert f'transactions/modify_{t_item}.html' in (t.name for t in response.templates)
    assert 'partials/_dash_menu.html' in (t.name for t in response.templates)
    assert f"Account: {user.username}" in response.content.decode('UTF-8')


@pytest.mark.django_db
def test_add_transaction(client, prepare_data):
    user = prepare_data["user"]
    client.force_login(user)
    category = prepare_data["category"]
    counterparty = prepare_data["counterparty"]
    wallet = prepare_data["wallet"]

    t_items_before = Transaction.objects.all().count()

    response = client.post(
        reverse(f'{app_name}:add_{t_item}'),
        {
            "date": "2022-10-10",
            "value": "997",
            "is_profit": 1,
            "category": category.pk,
            "counterparty": counterparty.pk,
            "owner": user.pk,
            "wallet": [wallet.pk],
        })

    t_items_after = Transaction.objects.all().count()

    assert response.status_code == 302
    assert response.url == reverse(f"{app_name}:list_{t_item}")
    assert t_items_after - t_items_before == 1


@pytest.mark.django_db
def test_modify_transaction(client, prepare_data):
    category = prepare_data["category"]
    counterparty = prepare_data["counterparty"]
    wallet = prepare_data["wallet"]
    initial_trans = prepare_data[t_item]

    user = prepare_data["user"]
    client.force_login(user)

    response = client.post(
        reverse(f'{app_name}:modify_{t_item}', args=f"{initial_trans.pk}"),
        {
            "date": "2022-10-10",
            "value": "100",
            "is_profit": 1,
            "category": category.pk,
            "counterparty": counterparty.pk,
            "owner": user.pk,
            "wallet": [wallet.pk],
        })

    updated_trans = Transaction.objects.get(pk=initial_trans.pk)
    assert response.url == reverse(f'{app_name}:list_{t_item}')
    assert updated_trans.value == 100


@pytest.mark.django_db
def test_delete_transaction(client, prepare_data):
    pk = prepare_data[t_item].pk
    user = prepare_data["user"]
    client.force_login(user)
    print(pk)
    t_items_before = Transaction.objects.all().count()

    response = client.post(
        reverse(f'{app_name}:modify_{t_item}', args=[f"{pk}"]), {"delete": ''})

    t_items_after = Transaction.objects.all().count()

    assert response.url == reverse(f"{app_name}:list_{t_item}")
    assert t_items_before - t_items_after == 1
    assert response.status_code == 302


@pytest.mark.django_db
def test_access_denied_if_not_logged_in(client, prepare_data):
    pk = prepare_data[t_item].pk

    client.logout()

    commands = [
        client.get(reverse(f'{app_name}:add_{t_item}')),
        client.get(reverse(f'{app_name}:list_{t_item}')),
        client.get(reverse(f'{app_name}:modify_{t_item}', args=[f"{pk}"])),

        client.post(reverse(f'{app_name}:add_{t_item}')),
        client.post(reverse(f'{app_name}:modify_{t_item}', args=[f"{pk}"])),
        client.post(reverse(f'{app_name}:modify_{t_item}', args=[f"{pk}"]), {"delete": ''}),
    ]

    for comm in commands:
        response = comm

        assert response.status_code == 302
        assert reverse('login') in response.url


@pytest.mark.django_db
def test_access_denied_if_different_user(client, prepare_data):
    pk = prepare_data[t_item].pk

    client.logout()
    user2 = get_user_model()(username="intruder")
    user2.save()
    client.force_login(user2)

    commands = [
        client.get(reverse(f'{app_name}:modify_{t_item}', args=[f"{pk}"])),

        client.post(reverse(f'{app_name}:add_{t_item}')),
        client.post(reverse(f'{app_name}:modify_{t_item}', args=[f"{pk}"])),
        client.post(reverse(f'{app_name}:modify_{t_item}', args=[f"{pk}"]), {"delete": ''}),
    ]

    for comm in commands:
        response = comm

        assert response.status_code == 302
        assert response.url == reverse(f'{app_name}:list_{t_item}')
