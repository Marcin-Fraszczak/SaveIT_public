# Generated by Django 4.1.3 on 2022-12-15 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('counterparties', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='counterparty',
            name='description',
            field=models.CharField(default='', max_length=80),
        ),
    ]