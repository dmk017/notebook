# Generated by Django 3.2.22 on 2023-11-14 17:55

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("address", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="address",
            options={"verbose_name_plural": "Адрес"},
        ),
        migrations.AlterModelOptions(
            name="country",
            options={"verbose_name_plural": "Страна"},
        ),
    ]
