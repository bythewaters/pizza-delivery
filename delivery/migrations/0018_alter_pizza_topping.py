# Generated by Django 4.1.6 on 2023-02-24 19:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("delivery", "0017_alter_pizza_topping"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pizza",
            name="topping",
            field=models.ManyToManyField(
                related_name="pizza_topping", to="delivery.topping"
            ),
        ),
    ]