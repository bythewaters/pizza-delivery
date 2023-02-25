from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from delivery.models import (
    Customer,
    FeedBack,
    Topping,
    Pizza,
    PizzaType,
    Order, Receipt
)


@admin.register(Customer)
class CustomerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("address", "phone_number",)
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
                        "phone_number",
                        "email"
                    )
                },
            ),
        )
    )


@admin.register(FeedBack)
class FeedBackAdmin(ModelAdmin):
    list_display = ("comment", "created_time", "customer")
    ordering = ("created_time",)


@admin.register(Topping)
class ToppingAdmin(ModelAdmin):
    list_display = ("name", "price")
    ordering = ("price",)


@admin.register(Pizza)
class PizzaAdmin(ModelAdmin):
    list_display = ("name", "price", "ingredients")
    ordering = ("price",)


@admin.register(PizzaType)
class PizzaTypeAdmin(ModelAdmin):
    list_display = ("type",)


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ("customer", "status")


admin.site.register(Receipt)
admin.site.unregister(Group)
