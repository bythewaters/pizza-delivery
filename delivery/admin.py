from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin

from delivery.models import (
    Customer,
    FeedBack,
    Ingredients,
    Pizza,
    PizzaType
)


@admin.register(Customer)
class CustomerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("address", "phone_number")
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("address", "phone_number")}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "address",
                        "phone_number"
                    )
                },
            ),
        )
    )


@admin.register(FeedBack)
class FeedBackAdmin(ModelAdmin):
    list_display = ("comment", "created_time", "customer")
    ordering = ("created_time",)


@admin.register(Ingredients)
class IngredientsAdmin(ModelAdmin):
    list_display = ("name", "price")
    ordering = ("price",)


@admin.register(Pizza)
class PizzaAdmin(ModelAdmin):
    list_display = ("name", "price", "ingredients")
    ordering = ("price",)


@admin.register(PizzaType)
class PizzaTypeAdmin(ModelAdmin):
    list_display = ("type",)
