from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from delivery.models import Customer

User = get_user_model()


class CustomerInfoUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["phone_number", "email", "address"]


class CustomerCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Customer
        fields = UserCreationForm.Meta.fields + (
            "phone_number",
            "address",
            "email",
            "first_name",
            "last_name"
        )
