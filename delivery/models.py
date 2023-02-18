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
        return reverse("delivery:customer-detail", kwargs={"pk": self.pk})

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


class Topping(models.Model):
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
    ingredients = models.TextField(blank=True, null=True)
    topping = models.ManyToManyField(Topping, related_name="pizza_topping")
    quantity = models.IntegerField(default=1)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}: {self.price}"


class Order(models.Model):
    pizza = models.ManyToManyField(Pizza, related_name="order")
    status = models.BooleanField(default=False)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.pizza.name}"


class Receipt(models.Model):
    customer_order = models.ForeignKey(Order, on_delete=models.CASCADE)
    order_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Receipt #{self.pk} ({self.order_time})"
