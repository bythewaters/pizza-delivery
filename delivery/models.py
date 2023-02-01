from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from delivery_pizza import settings


class Customer(AbstractUser):
    address = models.CharField(max_length=255, blank=False, null=False)
    phone_number = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        verbose_name = "customer"
        ordering = ["username"]

    def get_absolute_url(self):
        return reverse("taxi:driver-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return (
            f"{self.first_name} "
            f"{self.last_name} "
            f"{self.email} "
            f"{self.address} "
            f"{self.phone_number}"
        )


class FeedBack(models.Model):
    comment = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="feedback",
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["created_time"]


class PizzaType(models.Model):
    type = models.CharField(max_length=63)

    def __str__(self):
        return f"{self.type}"


class Ingredients(models.Model):
    name = models.CharField(max_length=63)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        ordering = ["price"]

    def __str__(self):
        return f"{self.name}: {self.price}"


class Pizza(models.Model):
    name = models.CharField(max_length=63)
    type_pizza = models.ForeignKey(PizzaType, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    ingredients = models.TextField()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}: {self.price}"
