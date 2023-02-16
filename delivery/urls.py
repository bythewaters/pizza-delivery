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
    OrderListView,
    AddToNewOrderView,
    OrderDeleteView,
    IncrementQuantityView,
    DecrementQuantityView,
    AddToToppingOrderView
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
    path("order/", OrderListView.as_view(), name="order-list"),
    path("order/add-pizza/<int:pizza_id>/", AddToNewOrderView.as_view(), name="order-add-pizza"),
    path("order/add-topping/<int:topping_id>/", AddToToppingOrderView.as_view(), name="order-add-topping"),
    path("order-delete/<int:pk>/", OrderDeleteView.as_view(), name="order-delete"),
    path("increment/<int:pk>/", IncrementQuantityView.as_view(), name="order-increment"),
    path("decrement/<int:pk>/", DecrementQuantityView.as_view(), name="order-decrement"),
]

app_name = "delivery"
