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
    OrderAddPizzaView,
    OrderDeleteView,
    IncrementQuantityView,
    DecrementQuantityView,
    FeedBackListView,
    create_receipt,
    ReceiptListView,
    clean_order, ChooseToppingView, add_toppings,
)

urlpatterns = [
    path("", index, name="index"),
    path("about/", about, name="about"),
    path("menu/", PizzaMenuListView.as_view(), name="pizza-menu-list"),
    path(
        "menu/type/<int:type_id>/",
        PizzaMenuListView.as_view(),
        name="pizza-menu-type-list",
    ),
    path(
        "menu/pizza/<int:pk>/update/",
        PizzaUpdateView.as_view(),
        name="pizza-update"
    ),
    path(
        "menu/create/",
        PizzaCreateView.as_view(),
        name="pizza-create"
    ),
    path(
        "menu/<int:pk>/delete/",
        PizzaDeleteView.as_view(),
        name="pizza-delete"
    ),
    path(
        "customer/<int:pk>/",
        CustomerDetailView.as_view(),
        name="customer-detail"
    ),
    path(
        "customer/<int:pk>/update/",
        CustomerUpdateView.as_view(),
        name="customer-update",
    ),
    path(
        "registration/",
        RegisterView.as_view(),
        name="customer-register"
    ),
    path(
        "topping/<int:pk>/update",
        ToppingUpdateView.as_view(),
        name="topping-update"
    ),
    path(
        "topping/create/",
        ToppingCreateView.as_view(),
        name="topping-create"
    ),
    path(
        "topping/<int:pk>/delete/",
        ToppingDeleteView.as_view(),
        name="topping-delete"
    ),
    path(
        "topping/",
        ToppingListView.as_view(),
        name="topping-list"
    ),
    path(
        "order/",
        OrderListView.as_view(),
        name="order-list"
    ),
    path(
        "order/add-pizza/<int:pizza_id>/",
        OrderAddPizzaView.as_view(),
        name="order-add-pizza",
    ),

    path(
        "order-delete/<int:order_id>/<int:pizza_id>/",
        OrderDeleteView.as_view(),
        name="order-delete",
    ),
    path(
        "increment/<int:pk>/",
        IncrementQuantityView.as_view(),
        name="order-increment"
    ),
    path(
        "decrement/<int:pk>/",
        DecrementQuantityView.as_view(),
        name="order-decrement"
    ),
    path("feedback/", FeedBackListView.as_view(), name="feedback-list"),
    path("create-receipt/", create_receipt, name="receipt-create"),
    path("receipt/", ReceiptListView.as_view(), name="receipt-list"),
    path("clean-order/<int:pk>/", clean_order, name="clean-order"),
    path("menu/add_toppings/<int:pizza_id>/", add_toppings, name="choose-topping"),
]

app_name = "delivery"
