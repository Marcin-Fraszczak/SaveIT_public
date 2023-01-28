"""
Scripts populating database with random data
"""
from random import randint, choice, choices
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model

from transactions.models import Transaction
from categories.models import Category
from counterparties.models import Counterparty
from wallets.models import Wallet

import os
from random import choices, randint

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


def create_categories():
    pass


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

    print(f'=' * 60)
    print("Created institutions:")

    print(f'=' * 60)



def populate_db():
    usernames = ["John", "Derek", "Maria", "Dude"]
    counterparties = ["Praca", "Enea", "Biedronka", "LIDL", "Auchan", "Żabka", "PKP", "Netia", "policja", "allegro"]
    categories = ["Praca", "Rozrywka", "Spożywka", "Chemia", "Sport", "Zdrowie"]
    wallets = ["Osobisty", "Rodzinny", "Firmowy"]

    def get_days_till_today(start):
        stop = datetime.now().date()
        delta = (stop - start).days
        return delta

    for username in usernames[:1]:
        # user creation
        user = get_user_model()(username=username, email=f"{username.split()[0]}@gmail.com")
        user.set_password('Testpass123')
        user.save()
        print(f"User {username} created.")

        # all other objects created for this user
        w_name = wallets[0].upper()
        w_unique_name = f"{user.username}_{w_name}"

        wallet = Wallet(name=w_name, unique_name=w_unique_name, owner=user)
        wallet.save()

        for c in counterparties:
            c_name = c.upper()
            c_unique_name = f"{user.username}_{c_name}"
            counterparty = Counterparty(name=c_name, unique_name=c_unique_name, owner=user)
            counterparty.save()

        for c in categories:
            c_name = c.upper()
            c_unique_name = f"{user.username}_{c_name}"
            category = Category(name=c_name, unique_name=c_unique_name, owner=user)
            category.save()

        starting_date = datetime(year=2022, month=1, day=1).date()
        _category = Category.objects.filter(owner=user)
        _counterparty = Counterparty.objects.filter(owner=user)
        _wallet = Wallet.objects.filter(owner=user)

        for i in range(get_days_till_today(starting_date)):

            today = starting_date + timedelta(days=i)

            if today.day == 10:
                transaction = Transaction(
                    counterparty=Counterparty.objects.get(name="PRACA"),
                    category=Category.objects.get(name="PRACA"),
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

        print(f"User {username} fully created.")


def say_hello():
    print("hello")


if __name__ == "__main__":
    say_hello()
