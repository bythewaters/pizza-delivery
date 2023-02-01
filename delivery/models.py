from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Customer(AbstractUser):
    address = models.CharField(max_length=255, blank=False, null=False)
    phone_number = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        verbose_name = "customer"
        ordering = ["username"]

    def get_absolute_url(self):
        return reverse("taxi:driver-detail", kwargs={"pk": self.pk})
