import pytest
from django.contrib.auth import get_user_model
from django.test import Client

from categories.models import Category
from counterparties.models import Counterparty
from transactions.models import Transaction
from wallets.models import Wallet
from plans.models import SavingsPlan


name = 'testuser'


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
def prepare_data(user):
    category = Category(
        name="test_cat".upper(),
        owner=user,
    )
    category.save()

    counterparty = Counterparty(
        name="test_cntp".upper(),
        owner=user,
    )
    counterparty.save()

    wallet = Wallet(
        name="test_wallet".upper(),
        owner=user,
    )
    wallet.save()

    transaction = Transaction(
        date="2022-10-11",
        value=998,
        is_profit=0,
        category=category,
        counterparty=counterparty,
        owner=user,
    )
    transaction.save()

    plan = SavingsPlan(
        name="test_plan".upper(),
        initial_value=1000,
        monthly_goal=2000,
        curve_type=1,
        owner=user,
    )
    plan.save()

    return {
        "category": category,
        "counterparty": counterparty,
        "savings_plan": plan,
        "transaction": transaction,
        "wallet": wallet,
        "user": user,
    }