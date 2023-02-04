from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

from delivery.models import Pizza, Ingredients, FeedBack, PizzaType, Customer


def index(request):
    pizza_count = Pizza.objects.count()
    topping_count = Ingredients.objects.count()
    feedback_count = FeedBack.objects.count()
    pizza_type_count = PizzaType.objects.count()

    context = {
        "pizza_count": pizza_count,
        "topping_count": topping_count,
        "feedback_count": feedback_count,
        "pizza_type_count": pizza_type_count
    }

    return render(request, "delivery/home.html", context=context)


def about(request):
    return render(request, "delivery/about_delivery.html")


class CustomerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Customer
    queryset = Customer.objects.all()


class PizzaMenuListView(LoginRequiredMixin, generic.ListView):
    model = Pizza
    pizza = Pizza.objects.select_related("type_pizza").distinct()
    template_name = "delivery/pizza_menu.html"
    context_object_name = "pizza_menu"