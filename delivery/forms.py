from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from delivery.models import Customer, FeedBack, Topping, Pizza


class CustomerInfoUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["phone_number", "email", "address"]

    def clean_phone_number(self) -> str:
        return validate_phone_number(self.cleaned_data["phone_number"])


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Customer
        fields = UserCreationForm.Meta.fields + (
            "phone_number",
            "address",
            "email",
            "first_name",
            "last_name"
        )

    def clean_phone_number(self) -> str:
        return validate_phone_number(self.cleaned_data["phone_number"])


class ToppingSearchForm(forms.Form):
    topping = forms.CharField(
        max_length=63,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search for name..."})
    )


class FeedBackCreateForm(forms.ModelForm):
    class Meta:
        model = FeedBack
        fields = ["comment"]


class PizzaForm(forms.ModelForm):
    topping = forms.ModelMultipleChoiceField(
        queryset=Topping.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        error_messages={"required": ""},
    )

    class Meta:
        model = Pizza
        fields = ("topping",)


def validate_phone_number(phone_number) -> str:
    if phone_number[:4] != "+380":
        raise ValidationError("Phone number must start with code +380")
    if len(phone_number) != 12:
        raise ValidationError("Phone number must have 11 digit")
    if not phone_number[5:13].isdigit():
        raise ValidationError("Phone number must have only digit")

    return phone_number
