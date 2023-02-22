from django import forms
from django.contrib.auth.forms import UserCreationForm
from delivery.models import Customer, FeedBack, Topping


class CustomerInfoUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["phone_number", "email", "address"]


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


class ToppingForm(forms.ModelForm):
    class Meta:
        model = Topping
        fields = ['name', 'price']

