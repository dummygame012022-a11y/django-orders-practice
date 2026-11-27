from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"{self.name} - {self.price}"


class Sale(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    def total(self):
        return sum(item.line_total() for item in self.items.all())

    def __str__(self):
        return f"Sale {self.pk}"


class SaleItem(models.Model):
    sale = models.ForeignKey(
        Sale, related_name="items", on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    qty = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True)

    def save(self, *args, **kwargs):
        if self.price is None:
            self.price = self.product.price
        super().save(*args, **kwargs)

    def line_total(self):
        return self.qty * self.price

    def __str__(self):
        return f"{self.product.name} x{self.qty}"
