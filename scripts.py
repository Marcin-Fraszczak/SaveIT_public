"""
Scripts populating database with random data
"""
import os
from random import randint, choice, choices
from datetime import datetime, timedelta

import django
from django.contrib.auth import get_user_model

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from categories.models import Category
from counterparties.models import Counterparty
from plans.models import SavingsPlan
from transactions.models import Transaction
from wallets.models import Wallet

User = get_user_model()


def check_if_taken(name, counter, admin=False):
    email = f'{name}{counter}@gmail.com'
    existing_users = User.objects.filter(email=email)
    if existing_users:
        counter += 1
        email = check_if_taken(name, counter, admin)
    return email, f'{name}{counter}'


def create_user(admin=False):
    try:
        admin = bool(admin)
    except Exception as e:
        print(e)
        return None

    if admin:
        name = "admin"
    else:
        name = "user"

    email, username = check_if_taken(name, 1, admin)
    password = "Testpass123"

    user = User(email=email, username=username)
    user.set_password(password)
    user.is_active = 1
    user.is_staff = admin
    user.is_superuser = admin
    user.save()

    return user, password


def create_categories(user):
    object_list = ["work", "fun", "food", "transportation", "sport", "housing", "health"]
    for obj in object_list:
        Category.objects.create(name=obj, unique_name=f'{user.username}_{obj}', owner=user)
        print(obj)


def create_counterparties(user):
    object_list = ["work", "Biedronka", "LIDL", "Tesco", "Post", "TM", "Lufthansa", "PGNiG"]
    for obj in object_list:
        Counterparty.objects.create(name=obj, unique_name=f'{user.username}_{obj}', owner=user)
        print(obj)


def create_wallets(user):
    object_list = ["Personal", "Company"]
    for obj in object_list:
        Wallet.objects.create(
            name=obj,
            unique_name=f'{user.username}_{obj}',
            owner=user,
            is_default=(obj == "Personal")
        )
        print(obj)


def create_plans(user):
    object_dict = {
        "Minimalist": {"goal": 4000, "init": 1000, "curve": 1},
        "Hedonist": {"goal": 6000, "init": 1200, "curve": 2},
        "Like No Tomorrow": {"goal": 12000, "init": 4000, "curve": 3},
    }
    for obj in object_dict:
        SavingsPlan.objects.create(
            name=obj,
            unique_name=f'{user.username}_{obj}',
            owner=user,
            is_default=(obj == "Minimalist"),
            monthly_goal=object_dict[obj]["goal"],
            initial_value=object_dict[obj]["init"],
            curve_type=object_dict[obj]["curve"],
        )
        print(obj)


def create_transactions(user):
    def get_days_till_today(start):
        stop = datetime.now().date()
        delta = (stop - start).days
        return delta

    starting_date = datetime(year=2022, month=6, day=1).date()
    _category = Category.objects.filter(owner=user)
    _counterparty = Counterparty.objects.filter(owner=user)
    _wallet = Wallet.objects.filter(owner=user)

    for i in range(get_days_till_today(starting_date)):

        today = starting_date + timedelta(days=i)

        if today.day == 10:
            transaction = Transaction(
                counterparty=Counterparty.objects.get(name="WORK"),
                category=Category.objects.get(name="WORK"),
                is_profit=True,
                value=6000,
                date=today,
                owner=user,
            )
            transaction.save()
            transaction.wallet.add(choice(_wallet))
            transaction.save()

        trans_no = randint(0, 3)
        if not trans_no:
            continue

        for t in range(trans_no):

            is_profit = choices([False, True], weights=[9, 1])[0]
            value = randint(5, 200)
            if not is_profit:
                value = -value

            transaction = Transaction(
                counterparty=choice(_counterparty),
                category=choice(_category),
                is_profit=is_profit,
                value=value,
                date=today,
                owner=user,
            )
            transaction.save()
            transaction.wallet.add(choice(_wallet))
            transaction.save()


def populate():
    print(f'=' * 60)
    user, password = create_user(admin=False)
    print(f'User created:')
    print(f'email: \t {user.username}')
    print(f'password: {password}')
    print(f'email: \t {user.email}')
    print(f'=' * 60)
    superuser, password = create_user(admin=True)
    print(f'Superuser created:')
    print(f'email: \t {superuser.username}')
    print(f'password: {password}')
    print(f'email: \t {superuser.email}')
    print(f'=' * 60)
    print("Created categories:")
    create_categories(user)
    print(f'=' * 60)
    print("Created counterparties:")
    create_counterparties(user)
    print(f'=' * 60)
    print("Created wallets:")
    create_wallets(user)
    print(f'=' * 60)
    print("Created plans:")
    create_plans(user)
    print(f'=' * 60)
    create_transactions(user)
    transactions = Transaction.objects.all().count()
    print(f"Created transactions: {transactions}")
    print(f'=' * 60)


def say_hello():
    print("hello")


if __name__ == "__main__":
    say_hello()
