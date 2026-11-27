from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .models import Product, Sale, SaleItem


@login_required
def product_list(request):
    products = Product.objects.select_related("category").all()
    return render(request, "pos/product_list.html", {"products": products})


@login_required
def sale_new(request):
    products = Product.objects.select_related("category").all()
    error = None
    if request.method == "POST":
        lines = []
        for p in products:
            raw = request.POST.get(f"qty_{p.pk}", "0")
            try:
                qty = int(raw)
            except ValueError:
                qty = 0
            if qty > 0:
                lines.append((p, qty))
        if lines:
            with transaction.atomic():
                sale = Sale.objects.create()
                for p, qty in lines:
                    SaleItem.objects.create(sale=sale, product=p, qty=qty)
            return redirect("sale_detail", pk=sale.pk)
        error = "Pili ug labing menos usa ka produkto."
    return render(
        request, "pos/sale_form.html", {"products": products, "error": error}
    )


@login_required
def sale_detail(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    return render(request, "pos/sale_detail.html", {"sale": sale})
