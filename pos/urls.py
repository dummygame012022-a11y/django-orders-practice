from django.urls import path

from . import views

urlpatterns = [
    path("products/", views.product_list, name="product_list"),
    path("sale/new/", views.sale_new, name="sale_new"),
    path("sale/<int:pk>/", views.sale_detail, name="sale_detail"),
]
