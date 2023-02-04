from django.urls import path, include

from delivery.views import index, about, PizzaMenuListView

urlpatterns = [
    path("", index, name="index"),
    path("about/", about, name="about"),
    path("menu/", PizzaMenuListView.as_view(), name="pizza-menu-list")
]

app_name = "delivery"
