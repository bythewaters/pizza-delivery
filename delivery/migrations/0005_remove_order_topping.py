# Generated by Django 4.1.6 on 2023-02-11 21:02

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("delivery", "0004_alter_payment_customer_order"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="topping",
        ),
    ]