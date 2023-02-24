from django.test import TestCase
from django.contrib.auth import get_user_model

from delivery.models import (
    FeedBack,
    PizzaType,
    Topping,
    Pizza,
    Order,
    Receipt
)


class CustomerModelTest(TestCase):
    def setUp(self) -> None:
        self.customer = get_user_model().objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass",
            address="Test Address",
            phone_number="123-456-7890",
        )

    def test_customer_str(self) -> None:
        self.assertEqual(
            str(self.customer),
            (
                f"{self.customer.first_name} "
                f"{self.customer.last_name} "
                f"{self.customer.email} "
                f"{self.customer.address} "
                f"{self.customer.phone_number}"
            ),
        )

    def test_get_customer_absolute_url(self) -> None:
        self.assertEqual(self.customer.get_absolute_url(), "/customer/1/")


class FeedBackModelTest(TestCase):
    def setUp(self) -> None:
        self.customer = get_user_model().objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass",
            address="Test Address",
            phone_number="123-456-7890",
        )
        self.feedback = FeedBack.objects.create(
            comment="Test Feedback", customer=self.customer
        )

    def test_feedback_creation(self):
        self.assertEqual(self.feedback.comment, "Test Feedback")
        self.assertEqual(self.feedback.customer, self.customer)


class PizzaTypeModelTest(TestCase):
    def setUp(self) -> None:
        self.pizza_type = PizzaType.objects.create(type="Test Pizza Type")

    def test_pizza_type_str(self) -> None:
        self.assertEqual(str(self.pizza_type), "Test Pizza Type")


class ToppingModelTestCase(TestCase):
    def setUp(self) -> None:
        self.topping = Topping.objects.create(name="Test Topping", price=9.99)

    def test_topping_str(self) -> None:
        self.assertEqual(str(self.topping), "Test Topping: 9.99")


class PizzaModelTestCase(TestCase):
    def setUp(self) -> None:
        self.pizza_type = PizzaType.objects.create(type="Test Pizza Type")
        self.topping = Topping.objects.create(name="Test Topping", price=9.99)
        self.pizza = Pizza.objects.create(
            name="Test Pizza", type_pizza=self.pizza_type, price=10.99
        )
        self.pizza.topping.add(self.topping)

    def test_pizza_creation(self) -> None:
        self.assertEqual(self.pizza.topping.first(), self.topping)
        self.assertEqual(str(self.pizza), "Test Pizza: 10.99")


class OrderModelTest(TestCase):
    def setUp(self) -> None:
        self.customer = get_user_model().objects.create_user(
            username="testuser",
        )
        self.pizza_type = PizzaType.objects.create(type="Test Pizza Type")
        self.topping = Topping.objects.create(name="Test Topping", price=9.99)
        self.pizza = Pizza.objects.create(
            name="Test Pizza", type_pizza=self.pizza_type, price="12.99"
        )
        self.order = Order.objects.create(customer=self.customer)
        self.order.pizza.add(self.pizza)

    def test_order_str(self) -> None:
        self.assertEqual(str(self.order.pizza.first().name), "Test Pizza")


class ReceiptModelTest(TestCase):
    def setUp(self) -> None:
        self.customer = get_user_model().objects.create_user(
            username="testuser",
        )
        self.pizza_type = PizzaType.objects.create(type="Test Pizza Type")
        self.pizza = Pizza.objects.create(
            name="test_pizza", price="12", type_pizza=self.pizza_type
        )
        self.order = Order.objects.create(customer=self.customer)
        self.order.pizza.add(self.pizza)
        self.receipt = Receipt.objects.create(
            customer_order=self.order,
        )

    def test_receipt_str(self) -> None:
        self.assertEqual(
            str(self.receipt),
            f"Receipt #{self.receipt.pk} "
            f"({self.receipt.order_time})"
        )
