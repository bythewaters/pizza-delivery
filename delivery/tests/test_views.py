from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from delivery.forms import CustomerInfoUpdateForm
from delivery.models import (
    PizzaType,
    Topping,
    Pizza,
    Order,
    Receipt,
    Customer,
)


class PublicCustomerDetailTest(TestCase):
    def test_login_required(self) -> None:
        response = self.client.get(
            reverse("delivery:customer-detail", args=[1])
        )
        self.assertNotEqual(response.status_code, 200)


class PrivateCustomerDetailTest(TestCase):
    def setUp(self) -> None:
        self.customer = get_user_model().objects.create(
            username="Test.test",
            phone_number="+380754672345",
            address="Test, 1, 234",
            email="test@gmail.com",
        )
        self.url = reverse("delivery:customer-detail", args=[self.customer.id])
        self.client.force_login(self.customer)

    def test_retrieve_customer_detail(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.customer.username)
        self.assertContains(response, self.customer.phone_number)
        self.assertContains(response, self.customer.address)
        self.assertContains(response, self.customer.email)


class PublicCustomerUpdateTest(TestCase):
    def test_login_required(self) -> None:
        response = self.client.get(
            reverse("delivery:customer-update", args=[1])
        )
        self.assertNotEqual(response.status_code, 200)


class PrivateCustomerUpdateTest(TestCase):
    def setUp(self) -> None:
        self.customer = get_user_model().objects.create(
            username="Test.test",
            phone_number="+380754672345",
            address="Test, 1, 234",
            email="test@gmail.com",
        )
        self.url = reverse("delivery:customer-update", args=[self.customer.id])
        self.client.force_login(self.customer)

    def test_retrieve_customer_update(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.customer.phone_number)
        self.assertContains(response, self.customer.address)
        self.assertContains(response, self.customer.email)

    def test_customer_update_form_valid(self) -> None:
        data = {
            "username": "Test2.test2",
            "phone_number": "+380754672346",
            "address": "Test2, 2, 345",
            "email": "test2@gmail.com",
        }
        form = CustomerInfoUpdateForm(data=data)
        self.assertTrue(form.is_valid())
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        customer = Customer.objects.last()
        self.assertEqual(customer.phone_number, data["phone_number"])
        self.assertEqual(customer.address, data["address"])
        self.assertEqual(customer.email, data["email"])
        self.assertRedirects(
            response, reverse("delivery:customer-detail", args=[customer.pk])
        )


class PrivatePizzaMenuTest(TestCase):
    def setUp(self) -> None:
        self.customer = get_user_model().objects.create(
            username="Test.test",
            phone_number="+380754672345",
            address="Test, 1, 234",
            email="test@gmail.com",
        )
        self.pizza_type1 = PizzaType.objects.create(type="TypeTest1")
        self.pizza_type2 = PizzaType.objects.create(type="TypeTest2")
        self.pizza1 = Pizza.objects.create(
            name="test", price="12", type_pizza=self.pizza_type1
        )
        self.pizza2 = Pizza.objects.create(
            name="test1", price="121", type_pizza=self.pizza_type2
        )
        self.url = reverse("delivery:pizza-menu-list")
        self.client.force_login(self.customer)

    def test_retrieve_pizza_menu_list(self) -> None:
        response = self.client.get(self.url)
        pizza_list = Pizza.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["pizza_menu"]), list(pizza_list)
        )
        self.assertTemplateUsed(
            response, "delivery/pizza_menu.html"
        )

    def test_get_context_data_pizza_menu(self) -> None:
        pizza_type = PizzaType.objects.all()
        response = self.client.get(self.url)
        self.assertEqual(
            list(response.context["pizza_type"]), list(pizza_type)
        )
        self.assertTemplateUsed(response, "delivery/pizza_menu.html")

    def test_get_queryset_pizza_menu(self) -> None:
        url = reverse(
            "delivery:pizza-menu-type-list",
            args=[self.pizza_type1.id]
        )
        response = self.client.get(url)
        self.assertContains(response, self.pizza1.name)
        self.assertNotContains(response, self.pizza2.name)
        self.assertTemplateUsed(response, "delivery/pizza_menu.html")


class PublicPizzaMenuTest(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("delivery:pizza-menu-list"))
        self.assertNotEqual(response.status_code, 200)


class PrivateToppingTest(TestCase):
    def setUp(self) -> None:
        self.customer = get_user_model().objects.create(
            username="Test.test",
            phone_number="+380754672345",
            address="Test, 1, 234",
            email="test@gmail.com",
        )
        self.pizza_type1 = PizzaType.objects.create(type="TypeTest1")
        self.pizza_type2 = PizzaType.objects.create(type="TypeTest2")
        self.pizza1 = Pizza.objects.create(
            name="test", price="12", type_pizza=self.pizza_type1
        )
        self.pizza2 = Pizza.objects.create(
            name="test1", price="121", type_pizza=self.pizza_type2
        )
        self.topping1 = Topping.objects.create(
            name="Test_topping1", price=1
        )
        self.topping2 = Topping.objects.create(
            name="Test_topping2", price=2
        )
        self.pizza1.topping.add(self.topping1)
        self.pizza2.topping.add(self.topping2)
        self.url = reverse("delivery:topping-list")
        self.client.force_login(self.customer)

    def test_retrieve_topping_list(self) -> None:
        response = self.client.get(self.url)
        topping_list = Topping.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["topping_list"]), list(topping_list)
        )
        self.assertTemplateUsed(response, "delivery/topping_list.html")

    def test_search_topping_form(self) -> None:
        response = self.client.get(self.url + "?topping=Test_topping1")
        self.assertContains(response, "Test_topping1")
        self.assertNotContains(response, "Test_topping2")
        self.assertTemplateUsed(response, "delivery/topping_list.html")


class PublicToppingTest(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("delivery:topping-list"))
        self.assertNotEqual(response.status_code, 200)


class PrivateOrderListTest(TestCase):
    def setUp(self) -> None:
        self.customer = get_user_model().objects.create(
            username="Test.test",
            phone_number="+380754672345",
            address="Test, 1, 234",
            email="test@gmail.com",
        )
        self.pizza_type1 = PizzaType.objects.create(type="TypeTest1")
        self.pizza_type2 = PizzaType.objects.create(type="TypeTest2")
        self.pizza1 = Pizza.objects.create(
            name="test", price=12, type_pizza=self.pizza_type1, quantity=1
        )
        self.pizza2 = Pizza.objects.create(
            name="test1", price=12, type_pizza=self.pizza_type2, quantity=2
        )
        self.topping1 = Topping.objects.create(
            name="Test_topping1", price=1
        )
        self.topping2 = Topping.objects.create(
            name="Test_topping2", price=2
        )
        self.pizza1.topping.add(self.topping1)
        self.pizza2.topping.add(self.topping2)
        self.order = Order.objects.create(customer=self.customer)
        self.order.pizza.add(self.pizza1)
        self.order.pizza.add(self.pizza2)
        self.url = reverse("delivery:order-list")
        self.client.force_login(self.customer)

    def test_retrieve_order_list(self) -> None:
        response = self.client.get(self.url)
        order_list = Order.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["orders"]), list(order_list))
        self.assertTemplateUsed(response, "delivery/order_list.html")

    def test_receipt_list_view_context_data(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "delivery/order_list.html")
        self.assertEqual(response.context["total_price"], 40)

    def test_clean_order(self) -> None:
        self.assertEqual(self.order.pizza.count(), 2)
        url = reverse("delivery:clean-order", args=[self.order.id])
        response = self.client.post(url)
        self.assertEqual(self.order.pizza.count(), 0)
        self.assertRedirects(response, "/")

    def test_increment_quantity_pizza_in_order(self) -> None:
        self.assertEqual(self.pizza1.quantity, 1)
        url = reverse("delivery:order-increment", args=[self.pizza1.id])
        response = self.client.post(url)
        updated_pizza = Pizza.objects.get(id=self.pizza1.id)
        self.assertEqual(updated_pizza.quantity, 2)
        self.assertRedirects(response, "/order/")

    def test_decrement_quantity_pizza_in_order(self) -> None:
        self.assertEqual(self.pizza2.quantity, 2)
        url = reverse("delivery:order-decrement", args=[self.pizza2.id])
        response = self.client.post(url)
        updated_pizza = Pizza.objects.get(id=self.pizza2.id)
        self.assertEqual(updated_pizza.quantity, 1)
        self.assertRedirects(response, "/order/")


class PublicOrderListTest(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("delivery:order-list"))
        self.assertNotEqual(response.status_code, 200)


class PublicFeedbackListTest(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("delivery:feedback-list"))
        self.assertEqual(response.status_code, 200)


class ReceiptListTest(TestCase):
    def setUp(self) -> None:
        self.customer = get_user_model().objects.create(
            username="Test.test",
            phone_number="+380754672345",
            address="Test, 1, 234",
            email="test@gmail.com",
        )
        self.pizza_type1 = PizzaType.objects.create(type="TypeTest1")
        self.pizza_type2 = PizzaType.objects.create(type="TypeTest2")
        self.pizza1 = Pizza.objects.create(
            name="test", price=12, type_pizza=self.pizza_type1
        )
        self.pizza2 = Pizza.objects.create(
            name="test1", price=12, type_pizza=self.pizza_type2
        )
        self.topping1 = Topping.objects.create(
            name="Test_topping1", price=1
        )
        self.topping2 = Topping.objects.create(
            name="Test_topping2", price=2
        )
        self.pizza1.topping.add(self.topping1)
        self.pizza2.topping.add(self.topping2)
        self.order = Order.objects.create(customer=self.customer)
        self.order.pizza.add(self.pizza1)
        self.order.pizza.add(self.pizza2)
        self.receipt1 = Receipt.objects.create(customer_order=self.order)
        self.url = reverse("delivery:receipt-list")
        self.client.force_login(self.customer)

    def test_receipt_list_view_context_data(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "delivery/receipt_list.html")
        self.assertEqual(response.context["total_price"], 28)
        self.assertEqual(response.context["topping_total_price"], 3)

    def test_create_receipt(self) -> None:
        self.assertEqual(Receipt.objects.all().count(), 1)
        url = reverse("delivery:receipt-create")
        response = self.client.post(url)
        self.assertRedirects(response, "/receipt/")
        self.assertEqual(Receipt.objects.all().count(), 2)
