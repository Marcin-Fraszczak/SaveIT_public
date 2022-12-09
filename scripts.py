"""
Scripts populating database with random data
"""
from random import randint, choice, choices, shuffle
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from transactions import models


def populate_db():
    usernames = ["John", "Derek", "Maria", "Dude"]
    counterparties = ["Enea", "Biedronka", "LIDL", "Auchan", "Żabka", "PKP", "Netia", "policja", "allegro"]
    categories = ["Rozrywka", "Spożywka", "Chemia", "Sport", "Zdrowie"]
    wallets = ["Osobisty", "Rodzinny", "Firmowy"]
    desc = 'aaeeoouuiibnvmcxzhshfkjeiroeqwertyuipkndkajkv'

    def random_desc():
        return "".join(choices(desc, k=randint(4, 20)))

    def random_date():
        start = datetime(year=2022, month=8, day=1).date()
        stop = datetime(year=2022, month=11, day=11).date()
        delta = timedelta(days=randint(1, (stop - start).days))
        return start + delta

    for username in usernames[:1]:
        user = get_user_model()(username=username, email=f"{username.split()[0]}@gmail.com")
        user.set_password('Testpass123')
        user.save()
        print(f"User {username} created.")

        w_name = choice(wallets).upper()
        w_unique_name = f"{user.username}_{w_name}"

        wallet = models.Wallet(name=w_name, unique_name=w_unique_name, description=random_desc(), owner=user)
        wallet.save()

        shuffle(counterparties)
        for c in counterparties[:len(counterparties) - 2]:
            c_name = c.upper()
            c_unique_name = f"{user.username}_{c_name}"
            counterparty = models.Counterparty(name=c_name, unique_name=c_unique_name, description=random_desc(),
                                               owner=user)
            counterparty.save()

        shuffle(categories)
        for c in categories[:len(categories) - 1]:
            c_name = c.upper()
            c_unique_name = f"{user.username}_{c_name}"
            category = models.Category(name=c_name, unique_name=c_unique_name, description=random_desc(), owner=user)
            category.save()

        for i in range(randint(60, 70)):
            pass
            _category = models.Category.objects.filter(owner=user)
            _counterparty = models.Counterparty.objects.filter(owner=user)
            _wallet = models.Wallet.objects.filter(owner=user)

            is_profit = bool(randint(0, 1))
            value = randint(1, 200)
            if not is_profit:
                value = -value

            transaction = models.Transaction(
                counterparty=choice(_counterparty),
                category=choice(_category),
                is_profit=is_profit,
                value=value,
                date=random_date(),
                owner=user,
                notes=random_desc(),
            )
            transaction.save()
            transaction.wallet.add(choice(_wallet))
            transaction.save()

        print(f"User {username} fully created.")
