from django.contrib import admin
from . import models

admin.site.register(models.Transaction)
admin.site.register(models.Wallet)
admin.site.register(models.Category)
admin.site.register(models.Counterparty)
admin.site.register(models.SavingsPlan)
