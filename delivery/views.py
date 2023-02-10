from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from delivery.forms import (
    CustomerInfoUpdateForm,
    RegisterForm,
    IngredientSearchForm
)
from delivery.models import (
    Pizza,
    Ingredients,
    FeedBack,
    PizzaType,
    Customer, Cart
)


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
    # permission_required = ("delivery.add_pizza", "delivery.change_pizza", "delivery.delete_pizza")
    model = Pizza
    pizza = Pizza.objects.all()
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
    success_url = reverse_lazy("delivery:pizza-menu-list")
    template_name = "delivery/pizza_delete_form.html"


class IngredientsListView(LoginRequiredMixin, generic.ListView):
    model = Ingredients
    form_class = IngredientSearchForm
    queryset = Ingredients.objects.all()
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IngredientsListView, self).get_context_data(**kwargs)
        ingredients = self.request.GET.get("ingredients", "")
        context["ingredients_form"] = IngredientSearchForm(
            initial={"ingredients": ingredients}
        )
        return context

    def get_queryset(self):
        form = IngredientSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(
                name__icontains=form.cleaned_data["ingredients"]
            )
        return self.queryset


class IngredientsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    permission_required = "delivery.change_ingredients"
    model = Ingredients
    fields = "__all__"
    success_url = reverse_lazy("delivery:ingredients-list")
    template_name = "delivery/ingredients_update_create_form.html"


class IngredientsCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    permission_required = "delivery.add_ingredients"
    model = Ingredients
    fields = "__all__"
    success_url = reverse_lazy("delivery:ingredients-list")
    template_name = "delivery/ingredients_update_create_form.html"


class IngredientsDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    permission_required = "delivery.delete_ingredients"
    model = Ingredients
    fields = "__all__"
    success_url = reverse_lazy("delivery:ingredients-list")
    template_name = "delivery/ingredients_delete_form.html"


class CartListView(LoginRequiredMixin, generic.ListView):
    model = Cart
    cart = Cart.objects.all()
    template_name = "delivery/cart_list.html"
