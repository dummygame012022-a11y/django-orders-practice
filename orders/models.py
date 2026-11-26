from django.db import models

# Create your models here.


class Order(models.Model):
    order = models.CharField(max_length=50)
    item = models.CharField(max_length=100)
    qty = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.order} - {self.item} x{self.qty}"
