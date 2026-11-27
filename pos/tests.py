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


class ProductListTest(TestCase):
    def test_list_shows_product(self):
        c = Category.objects.create(name="Fake Drinks")
        Product.objects.create(
            name="Fake Coffee", price=Decimal("50.00"), category=c
        )
        response = self.client.get("/pos/products/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Fake Coffee - 50.00 (Fake Drinks)")

    def test_list_empty(self):
        response = self.client.get("/pos/products/")
        self.assertContains(response, "Walay produkto pa.")
