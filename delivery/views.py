from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic, View

from delivery.forms import (
    CustomerInfoUpdateForm,
    RegisterForm,
    ToppingSearchForm,
    FeedBackCreateForm,
    PizzaForm,
)
from delivery.models import (
    Pizza,
    Topping,
    FeedBack,
    PizzaType,
    Customer,
    Order,
    Receipt,
)


def index(request):
    pizza_count = Pizza.objects.count()
    topping_count = Topping.objects.count()
    feedback_count = FeedBack.objects.count()
    pizza_type_count = PizzaType.objects.count()

    context = {
        "pizza_count": pizza_count,
        "topping_count": topping_count,
        "feedback_count": feedback_count,
        "pizza_type_count": pizza_type_count,
    }

    return render(request, "delivery/home.html", context=context)


def about(request):
    return render(request, "delivery/about_delivery.html")


class CustomerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Customer
    queryset = Customer.objects.all()


class CustomerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Customer
    form_class = CustomerInfoUpdateForm
    template_name = "delivery/customer_update_form.html"

    def form_valid(self, form):
        valid_form = form.save(commit=False)
        valid_form.save()
        return redirect("delivery:customer-detail", self.object.pk)


class RegisterView(generic.CreateView):
    model = Customer
    form_class = RegisterForm
    template_name = "delivery/customer_register_form.html"

    def form_valid(self, form):
        form.save()
        user = authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password1"],
        )
        login(self.request, user)
        return HttpResponseRedirect(reverse("delivery:index"))


class PizzaMenuListView(LoginRequiredMixin, generic.ListView):
    model = Pizza
    pizza = Pizza.objects.select_related("type_pizza_id").prefetch_related("topping")
    template_name = "delivery/pizza_menu.html"
    context_object_name = "pizza_menu"

    def get_context_data(self, **kwargs):
        context = super(PizzaMenuListView, self).get_context_data(**kwargs)
        context["pizza_type"] = PizzaType.objects.all()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        try:
            search_term = self.kwargs["type_id"]
        except KeyError:
            return queryset
        if search_term is not None:
            queryset = queryset.filter(type_pizza=search_term)
        return queryset


class PizzaCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.CreateView
):
    permission_required = "delivery.add_pizza"
    model = Pizza
    fields = ["name", "type_pizza", "price", "ingredients"]
    success_url = reverse_lazy("delivery:pizza-menu-list")
    template_name = "delivery/pizza_update_create_form.html"


class PizzaUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.UpdateView
):
    permission_required = "delivery.change_pizza"
    model = Pizza
    fields = ["name", "type_pizza", "price", "ingredients"]
    success_url = reverse_lazy("delivery:pizza-menu-list")
    template_name = "delivery/pizza_update_create_form.html"


class PizzaDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.DeleteView
):
    permission_required = "delivery.delete_pizza"
    model = Pizza
    queryset = Pizza.objects.prefetch_related("order__pizza")
    success_url = reverse_lazy("delivery:pizza-menu-list")
    template_name = "delivery/pizza_delete_form.html"


class ToppingListView(LoginRequiredMixin, generic.ListView):
    model = Topping
    form_class = ToppingSearchForm
    queryset = Topping.objects.all()
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ToppingListView, self).get_context_data(**kwargs)
        topping = self.request.GET.get("topping", "")
        context["topping_form"] = ToppingSearchForm(
            initial={"topping": topping}
        )
        return context

    def get_queryset(self):
        form = ToppingSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(
                name__icontains=form.cleaned_data["topping"]
            )
        return self.queryset


class ToppingUpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView
):
    permission_required = "delivery.change_topping"
    model = Topping
    fields = "__all__"
    success_url = reverse_lazy("delivery:topping-list")
    template_name = "delivery/topping_update_create_form.html"


class ToppingCreateView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView
):
    permission_required = "delivery.add_topping"
    model = Topping
    fields = "__all__"
    success_url = reverse_lazy("delivery:topping-list")
    template_name = "delivery/topping_update_create_form.html"


class ToppingDeleteView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView
):
    permission_required = "delivery.delete_topping"
    model = Topping
    fields = "__all__"
    success_url = reverse_lazy("delivery:topping-list")
    template_name = "delivery/topping_delete_form.html"


class OrderListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = "delivery/order_list.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.select_related("customer").filter(customer=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        orders = self.get_queryset().prefetch_related("pizza")
        total_price = 0
        for order in orders:
            for pizza in order.pizza.all():
                total_price += pizza.price * pizza.quantity
                pizza.price_with_toppings = pizza.price * pizza.quantity
                pizza.save()
                if pizza.topping.all:
                    for topping in pizza.topping.all():
                        pizza.price_with_toppings += topping.price
                        total_price += topping.price
                        pizza.save()
        context["total_price"] = total_price
        return context


class OrderAddPizzaView(LoginRequiredMixin, View):
    @staticmethod
    def post(request, pizza_id):
        pizza = Pizza.objects.get(id=pizza_id)
        customer = request.user
        try:
            order = Order.objects.get(customer=customer)
        except Order.DoesNotExist:
            order = Order.objects.create(customer=customer)

        new_pizza = Pizza.objects.create(
            name=pizza.name,
            type_pizza=pizza.type_pizza,
            price=pizza.price,
            price_with_toppings=pizza.price_with_toppings,
            ingredients=pizza.ingredients,
            quantity=1,
            is_custom_pizza=True
        )

        order.pizza.add(new_pizza)

        return redirect("delivery:pizza-menu-list")


class OrderDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Order
    success_url = reverse_lazy("delivery:order-list")
    template_name = "delivery/order_list.html"

    def post(self, request, *args, **kwargs):
        pizza = Pizza.objects.get(id=kwargs.get("pizza_id"))
        order = Order.objects.get(id=kwargs.get("order_id"))
        order.pizza.remove(kwargs.get("pizza_id"))
        pizza.quantity = 1
        if pizza.topping.all():
            pizza.topping.clear()
        pizza.save()
        if order.pizza.count() == 0:
            order.delete()
        try:
            Pizza.objects.get(name=pizza.name)
        except Pizza.MultipleObjectsReturned:
            pizza.delete()
        return redirect("delivery:order-list")


class IncrementQuantityView(LoginRequiredMixin, View):
    @staticmethod
    def post(request, pk):
        pizza = Pizza.objects.get(id=pk)
        pizza.quantity += 1
        pizza.save()
        return redirect("delivery:order-list")


class DecrementQuantityView(LoginRequiredMixin, View):
    @staticmethod
    def post(request, pk):
        pizza = Pizza.objects.get(id=pk)
        if pizza.quantity > 1:
            pizza.quantity -= 1
            pizza.save()
        return redirect("delivery:order-list")


class FeedBackListView(LoginRequiredMixin, generic.ListView):
    model = FeedBack
    queryset = FeedBack.objects.select_related(
        "customer"
    ).order_by("-created_time")
    template_name = "delivery/feedback.html"
    paginate_by = 3

    def post(self, request):
        form = FeedBackCreateForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.customer = self.request.user
            feedback.save()
        return redirect("delivery:feedback-list")


def create_receipt(request):
    order = Order.objects.filter(
        customer=request.user, status=False
    ).first()
    if order:
        Receipt.objects.create(customer_order=order)
        order.status = True
        order.save()
    return redirect("delivery:receipt-list")


class ReceiptListView(LoginRequiredMixin, generic.ListView):
    model = Receipt
    receipt = Receipt.objects.select_related(
        "customer_order"
    ).prefetch_related(
        "customer_order__pizza"
    )
    template_name = "delivery/receipt_list.html"
    context_object_name = "receipt_order"

    def get_queryset(self):
        return Receipt.objects.filter(
            customer_order__customer=self.request.user
        ).order_by("-order_time")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ReceiptListView, self).get_context_data(**kwargs)
        order = self.get_queryset().prefetch_related("customer_order__pizza")
        total_price = 0
        topping_total_price = 0
        for order in order:
            for pizza in order.customer_order.pizza.all():
                total_price += pizza.price * pizza.quantity
                pizza.price_with_toppings = pizza.price * pizza.quantity
                pizza.save()
                for topping in pizza.topping.all():
                    pizza.price_with_toppings += topping.price
                    topping_total_price += topping.price
                    total_price += topping.price
                    pizza.save()
        context["total_price"] = total_price
        context["topping_total_price"] = topping_total_price
        return context


def clean_order(request, pk):
    order = Order.objects.get(id=pk)
    for pizza in order.pizza.all():
        try:
            pizza_to_delete = Pizza.objects.get(id=pizza.id)
            pizza_to_delete.delete()
        except Pizza.DoesNotExist:
            pass
        except Pizza.MultipleObjectsReturned:
            pass
    order.delete()
    return redirect(reverse_lazy("delivery:index"))


class ChooseToppingView(
    LoginRequiredMixin,
    generic.UpdateView
):
    model = Pizza
    form_class = PizzaForm
    success_url = reverse_lazy("delivery:order-list")
    template_name = "delivery/choose_toppings.html"
