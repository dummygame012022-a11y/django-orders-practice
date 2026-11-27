from django.shortcuts import render

from .models import Product


def product_list(request):
    products = Product.objects.select_related("category").all()
    return render(request, "pos/product_list.html", {"products": products})
