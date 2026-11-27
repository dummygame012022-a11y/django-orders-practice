from django.contrib import admin

from .models import Category, Product, Sale, SaleItem


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1


class SaleAdmin(admin.ModelAdmin):
    inlines = [SaleItemInline]


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Sale, SaleAdmin)
