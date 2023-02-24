from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from delivery.models import (
    FeedBack,
    PizzaType,
    Topping,
    Pizza,
    Order,
    Receipt
)
