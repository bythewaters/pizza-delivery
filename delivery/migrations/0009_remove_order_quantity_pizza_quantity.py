# Generated by Django 4.1.6 on 2023-02-13 19:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("delivery", "0008_alter_order_customer"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="quantity",
        ),
        migrations.AddField(
            model_name="pizza",
            name="quantity",
            field=models.IntegerField(default=1),
        ),
    ]
