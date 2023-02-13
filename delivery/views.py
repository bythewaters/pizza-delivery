from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic


from delivery.forms import (
    CustomerInfoUpdateForm,
    RegisterForm,
    ToppingSearchForm
)
from delivery.models import (
    Pizza,
    Topping,
    FeedBack,
    PizzaType,
    Customer,
    Order,
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
        "pizza_type_count": pizza_type_count
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
        self.object = form.save(commit=False)
        self.object.save()
        return redirect('delivery:customer-detail', self.object.pk)


class RegisterView(generic.CreateView):
    model = Customer
    form_class = RegisterForm
    template_name = "delivery/customer_register_form.html"

    def form_valid(self, form):
        form.save()
        user = authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password1"]
        )
        login(self.request, user)
        return HttpResponseRedirect(reverse("delivery:index"))


class PizzaMenuListView(LoginRequiredMixin, generic.ListView):
    model = Pizza
    pizza = Pizza.objects.select_related("type_pizza_id")
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


class PizzaCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    permission_required = "delivery.add_pizza"
    model = Pizza
    fields = "__all__"
    success_url = reverse_lazy("delivery:pizza-menu-list")
    template_name = "delivery/pizza_update_create_form.html"


class PizzaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    permission_required = "delivery.change_pizza"
    model = Pizza
    fields = "__all__"
    success_url = reverse_lazy("delivery:pizza-menu-list")
    template_name = "delivery/pizza_update_create_form.html"


class PizzaDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
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


class ToppingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    permission_required = "delivery.change_topping"
    model = Topping
    fields = "__all__"
    success_url = reverse_lazy("delivery:topping-list")
    template_name = "delivery/topping_update_create_form.html"


class ToppingCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    permission_required = "delivery.add_topping"
    model = Topping
    fields = "__all__"
    success_url = reverse_lazy("delivery:topping-list")
    template_name = "delivery/topping_update_create_form.html"


class ToppingDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    permission_required = "delivery.delete_topping"
    model = Topping
    fields = "__all__"
    success_url = reverse_lazy("delivery:topping-list")
    template_name = "delivery/topping_delete_form.html"


def order(request):
    # try:
    #     current_username = request.user.username
    #     user = User.objects.filter(username=current_username)
    #     orders = Order
    # except:
    #     pass
    return render(request, "delivery/order_list.html")
