from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from delivery.models import Customer


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
