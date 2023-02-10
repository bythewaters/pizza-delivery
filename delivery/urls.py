from django.urls import path

from delivery.views import (
    index,
    about,
    PizzaMenuListView,
    CustomerDetailView,
    CustomerUpdateView,
    IngredientsListView,
    IngredientsUpdateView,
    IngredientsCreateView,
    IngredientsDeleteView,
    RegisterView,
    PizzaUpdateView,
    PizzaCreateView,
    PizzaDeleteView,
    CartListView
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
    path("ingredients/<int:pk>/update", IngredientsUpdateView.as_view(), name="ingredients-update"),
    path("ingredients/create/", IngredientsCreateView.as_view(), name="ingredients-create"),
    path("ingredients/<int:pk>/delete/", IngredientsDeleteView.as_view(), name="ingredients-delete"),
    path("ingredients/", IngredientsListView.as_view(), name="ingredients-list"),
    path("cart/<int:pk>/", CartListView.as_view(), name="cart-list"),
]

app_name = "delivery"
