"""
Scripts populating database with random data
"""
from random import randint, choice, choices
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from transactions import models
from categories import models
from counterparties import models
from wallets import models
from plans import models


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

        wallet = models.Wallet(name=w_name, unique_name=w_unique_name, owner=user)
        wallet.save()

        for c in counterparties:
            c_name = c.upper()
            c_unique_name = f"{user.username}_{c_name}"
            counterparty = models.Counterparty(name=c_name, unique_name=c_unique_name, owner=user)
            counterparty.save()

        for c in categories:
            c_name = c.upper()
            c_unique_name = f"{user.username}_{c_name}"
            category = models.Category(name=c_name, unique_name=c_unique_name, owner=user)
            category.save()

        starting_date = datetime(year=2022, month=1, day=1).date()
        _category = models.Category.objects.filter(owner=user)
        _counterparty = models.Counterparty.objects.filter(owner=user)
        _wallet = models.Wallet.objects.filter(owner=user)

        for i in range(get_days_till_today(starting_date)):

            today = starting_date + timedelta(days=i)

            if today.day == 10:
                transaction = models.Transaction(
                    counterparty=models.Counterparty.objects.get(name="PRACA"),
                    category=models.Category.objects.get(name="PRACA"),
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

                is_profit = choices([False, True], weights=[9, 1])
                value = randint(5, 200)
                if not is_profit:
                    value = -value

                transaction = models.Transaction(
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
