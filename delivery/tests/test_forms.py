from django.test import TestCase
from delivery.forms import (
    CustomerInfoUpdateForm,
    RegisterForm,
)


class RegisterFormTest(TestCase):
    def test_customer_register(self) -> None:
        self.form_data = {
            "username": "test.test1",
            "password1": "Ab457363234",
            "password2": "Ab457363234",
            "first_name": "TestUser",
            "last_name": "UserTest",
            "phone_number": "+380752051423",
            "address": "test,2,3",
            "email": "test@gmail.com",
        }
        form = RegisterForm(data=self.form_data,)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.data, self.form_data)


class CustomerUpdateForm(TestCase):
    def test_update_phone_number(self) -> None:
        test_customer = {
            "phone_number": "+380752051423",
            "email": "test@gmail.com",
            "address": "test, 1, 234"
        }

        form = CustomerInfoUpdateForm(data=test_customer)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.data, test_customer)

    def test_check_valid_phone_number(self) -> None:
        test_first_phone_code = CustomerInfoUpdateForm(
            data={"phone_number": "+4802071324"}
        )

        test_len_phone_number = CustomerInfoUpdateForm(
            data={"phone_number": "+38020713"}
        )

        test_only_digits = CustomerInfoUpdateForm(
            data={"phone_number": "+38020713w4"}
        )

        self.assertFalse(test_first_phone_code.is_valid())
        self.assertFalse(test_len_phone_number.is_valid())
        self.assertFalse(test_only_digits.is_valid())
