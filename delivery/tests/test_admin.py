from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from delivery.models import (
    Customer,
    FeedBack,
    Topping,
    Pizza,
    PizzaType,
    Order
)


class DeliveryAdminTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin", email="admin@example.com", password="testpass"
        )
        self.client.force_login(self.admin_user)

    def test_customer_admin_display(self) -> None:
        customer = Customer.objects.create(
            username="testcustomer",
            email="testcustomer@example.com",
            address="123 Main St",
            phone_number="123-456-7890",
        )
        response = self.client.get(
            reverse("admin:delivery_customer_change", args=(customer.id,))
        )
        self.assertContains(response, customer.username)
        self.assertContains(response, customer.email)
        self.assertContains(response, customer.address)
        self.assertContains(response, customer.phone_number)

    def test_feedback_admin_display(self) -> None:
        feedback = FeedBack.objects.create(
            customer=self.admin_user, comment="Test comment"
        )
        response = self.client.get(
            reverse("admin:delivery_feedback_change", args=(feedback.id,))
        )
        self.assertContains(response, feedback.customer)
        self.assertContains(response, feedback.comment)

    def test_topping_admin_display(self) -> None:
        topping = Topping.objects.create(name="Test Topping", price=9.99)
        response = self.client.get(
            reverse("admin:delivery_topping_change", args=(topping.id,))
        )
        self.assertContains(response, topping.name)
        self.assertContains(response, topping.price)

    def test_pizza_admin_display(self) -> None:
        pizza_type = PizzaType.objects.create(type="Test Pizza Type")
        pizza = Pizza.objects.create(
            name="Test Pizza", type_pizza=pizza_type, price="12.99"
        )
        toppings = [
            Topping.objects.create(name=f"Topping {i}", price=i) for i in range(3)
        ]
        pizza.topping.set(toppings)
        response = self.client.get(
            reverse("admin:delivery_pizza_change", args=(pizza.id,))
        )
        self.assertContains(response, pizza.name)
        self.assertContains(response, pizza.price)
        for topping in pizza.topping.all():
            self.assertContains(response, topping.name)
            self.assertContains(response, topping.price)

    def test_pizza_type_admin_display(self) -> None:
        pizza_type = PizzaType.objects.create(type="Test Pizza Type")
        response = self.client.get(
            reverse("admin:delivery_pizzatype_change", args=(pizza_type.id,))
        )
        self.assertContains(response, pizza_type.type)

    def test_order_admin_display(self) -> None:
        customer = Customer.objects.create(
            username="testcustomer",
            email="testcustomer@example.com",
            address="123 Main St",
            phone_number="123-456-7890",
        )
        pizza_type = PizzaType.objects.create(type="Test Pizza Type")
        pizza = Pizza.objects.create(
            name="Test Pizza", type_pizza=pizza_type, price="12.99"
        )

        order = Order.objects.create(customer=customer)
        order.pizza.add(pizza)
        response = self.client.get(
            reverse("admin:delivery_order_change", args=(order.id,))
        )
        self.assertContains(response, order.customer)
