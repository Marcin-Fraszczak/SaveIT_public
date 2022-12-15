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

    wallet2 = Wallet(
        name="test_wallet2".upper(),
        owner=user,
    )
    wallet2.save()

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

    plan2 = SavingsPlan(
        name="test_plan2".upper(),
        initial_value=1000,
        monthly_goal=2000,
        curve_type=1,
        owner=user,
    )
    plan2.save()

    return {
        "category": category,
        "counterparty": counterparty,
        "savings_plan": plan,
        "savings_plan2": plan2,
        "transaction": transaction,
        "wallet": wallet,
        "wallet2": wallet2,
        "user": user,
    }


@pytest.fixture
def translate():
    return {
        "category": {
            # "count": Category.objects.all().count(),
            "model": Category,
            # "last": Category.objects.last(),
            "app": "categories",
        },
        "counterparty": {
            # "count": Counterparty.objects.all().count(),
            "model": Counterparty,
            # "last": Counterparty.objects.last(),
            "app": "counterparties",
        },
        "wallet": {
            # "count": Wallet.objects.all().count(),
            "model": Wallet,
            # "last": Wallet.objects.last(),
            "app": "wallets",
        },
        "savings_plan": {
            # "count": SavingsPlan.objects.all().count(),
            "model": SavingsPlan,
            # "last": SavingsPlan.objects.last(),
            "app": "plans",
        },
    }
