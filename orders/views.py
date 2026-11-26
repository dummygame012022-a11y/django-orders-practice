from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from .models import Order


def order_list(request):
    orders = Order.objects.all()
    return render(request, "orders/order_list.html", {"orders": orders})

from django.shortcuts import redirect
from .forms import OrderForm


def order_add(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("order_list")
    else:
        form = OrderForm()
    return render(request, "orders/order_form.html", {"form": form})

from django.shortcuts import get_object_or_404


def order_edit(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect("order_list")
    else:
        form = OrderForm(instance=order)
    return render(request, "orders/order_form.html", {"form": form})


def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        order.delete()
        return redirect("order_list")
    return render(request, "orders/order_confirm_delete.html", {"order": order})
