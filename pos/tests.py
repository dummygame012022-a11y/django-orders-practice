from decimal import Decimal

from django.test import TestCase

from .models import Category, Product


class PosModelTest(TestCase):
    def test_category_str(self):
        c = Category.objects.create(name="Fake Drinks")
        self.assertEqual(str(c), "Fake Drinks")

    def test_product_str(self):
        c = Category.objects.create(name="Fake Drinks")
        p = Product.objects.create(
            name="Fake Coffee", price=Decimal("50.00"), category=c
        )
        self.assertEqual(str(p), "Fake Coffee - 50.00")

    def test_delete_category_keeps_product(self):
        c = Category.objects.create(name="Fake Drinks")
        p = Product.objects.create(
            name="Fake Coffee", price=Decimal("50.00"), category=c
        )
        c.delete()
        p.refresh_from_db()
        self.assertIsNone(p.category)
