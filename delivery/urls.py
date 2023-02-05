from django.urls import path, include

from delivery.views import (
    index,
    about,
    PizzaMenuListView,
    PizzaTypeListView,
    PizzaDetailView,
    CustomerDetailView,
    CustomerUpdateView
)

urlpatterns = [
    path("", index, name="index"),
    path("about/", about, name="about"),
    path("menu/", PizzaMenuListView.as_view(), name="pizza-menu-list"),
    path("menu/pizza/<int:pk>/", PizzaDetailView.as_view(), name="pizza-detail"),
    path("customer/<int:pk>/", CustomerDetailView.as_view(), name="customer-detail"),
    path("customer/<int:pk>/update/", CustomerUpdateView.as_view(), name="customer-update"),
    path("menu/", PizzaTypeListView.as_view(), name="pizza-type-list")
]

app_name = "delivery"
