from django.urls import path

from delivery.views import (
    index,
    about,
    PizzaMenuListView,
    CustomerDetailView,
    CustomerUpdateView,
    ToppingListView,
    ToppingUpdateView,
    ToppingCreateView,
    ToppingDeleteView,
    RegisterView,
    PizzaUpdateView,
    PizzaCreateView,
    PizzaDeleteView,
    order,
)

urlpatterns = [
    path("", index, name="index"),
    path("about/", about, name="about"),
    path("menu/", PizzaMenuListView.as_view(), name="pizza-menu-list"),
    path("menu/type/<int:type_id>/", PizzaMenuListView.as_view(), name="pizza-menu-type-list"),
    path("menu/pizza/<int:pk>/update/", PizzaUpdateView.as_view(), name="pizza-update"),
    path("menu/create/", PizzaCreateView.as_view(), name="pizza-create"),
    path("menu/<int:pk>/delete/", PizzaDeleteView.as_view(), name="pizza-delete"),
    path("customer/<int:pk>/", CustomerDetailView.as_view(), name="customer-detail"),
    path("customer/<int:pk>/update/", CustomerUpdateView.as_view(), name="customer-update"),
    path("registration/", RegisterView.as_view(), name="customer-register"),
    path("topping/<int:pk>/update", ToppingUpdateView.as_view(), name="topping-update"),
    path("topping/create/", ToppingCreateView.as_view(), name="topping-create"),
    path("topping/<int:pk>/delete/", ToppingDeleteView.as_view(), name="topping-delete"),
    path("topping/", ToppingListView.as_view(), name="topping-list"),
    path("order/", order, name="order-list"),
]

app_name = "delivery"
