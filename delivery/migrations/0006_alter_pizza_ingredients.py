# Generated by Django 4.1.6 on 2023-02-12 21:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("delivery", "0005_remove_order_topping"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pizza",
            name="ingredients",
            field=models.TextField(blank=True, null=True),
        ),
    ]
