from django.urls import path

from delivery.views import (
    index,
    about,
    PizzaMenuListView,
    PizzaDetailView,
    CustomerDetailView,
    CustomerUpdateView,
    IngredientsListView,
    RegisterView
)

urlpatterns = [
    path("", index, name="index"),
    path("about/", about, name="about"),
    path("menu/", PizzaMenuListView.as_view(), name="pizza-menu-list"),
    path("menu/type/<int:type_id>/", PizzaMenuListView.as_view(), name="pizza-menu-type-list"),
    path("menu/pizza/<int:pk>/", PizzaDetailView.as_view(), name="pizza-detail"),
    path("customer/<int:pk>/", CustomerDetailView.as_view(), name="customer-detail"),
    path("customer/<int:pk>/update/", CustomerUpdateView.as_view(), name="customer-update"),
    path("registration/", RegisterView.as_view(), name="customer-register"),
    path("ingredients/", IngredientsListView.as_view(), name="ingredients-list"),
]

app_name = "delivery"
