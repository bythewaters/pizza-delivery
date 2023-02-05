from django import forms
from django.core.exceptions import ValidationError

from delivery.models import Customer


class CustomerInfoUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["phone_number", "email", "address"]
