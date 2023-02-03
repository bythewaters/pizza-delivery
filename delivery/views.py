from django.shortcuts import render

from delivery.models import Pizza, Ingredients, FeedBack, PizzaType


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
    counter_pizza = Pizza.objects.count()
    print(counter_pizza)
    context = {
        "counter_pizza": counter_pizza
    }
    return render(request, "delivery/about_delivery.html", context)
