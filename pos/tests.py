from decimal import Decimal

from django.test import TestCase

from django.contrib.auth.models import User
from django.db.models import ProtectedError

from .models import Category, Product, Sale, SaleItem


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
    def setUp(self):
        self.client.force_login(User.objects.create_user("fakecashier"))

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


class SaleTest(TestCase):
    def setUp(self):
        self.coffee = Product.objects.create(
            name="Fake Coffee", price=Decimal("50.00")
        )
        self.tea = Product.objects.create(
            name="Fake Tea", price=Decimal("30.00")
        )

    def test_total(self):
        sale = Sale.objects.create()
        SaleItem.objects.create(sale=sale, product=self.coffee, qty=2)
        SaleItem.objects.create(sale=sale, product=self.tea, qty=1)
        self.assertEqual(sale.total(), Decimal("130.00"))

    def test_price_copied_from_product(self):
        sale = Sale.objects.create()
        item = SaleItem.objects.create(sale=sale, product=self.coffee, qty=1)
        self.assertEqual(item.price, Decimal("50.00"))

    def test_price_snapshot_does_not_change(self):
        sale = Sale.objects.create()
        item = SaleItem.objects.create(sale=sale, product=self.coffee, qty=1)
        self.coffee.price = Decimal("99.00")
        self.coffee.save()
        item.refresh_from_db()
        self.assertEqual(item.price, Decimal("50.00"))

    def test_cannot_delete_product_in_sale(self):
        sale = Sale.objects.create()
        SaleItem.objects.create(sale=sale, product=self.coffee, qty=1)
        with self.assertRaises(ProtectedError):
            self.coffee.delete()


class SalePageTest(TestCase):
    def setUp(self):
        self.client.force_login(User.objects.create_user("fakecashier"))
        self.coffee = Product.objects.create(
            name="Fake Coffee", price=Decimal("50.00")
        )
        self.tea = Product.objects.create(
            name="Fake Tea", price=Decimal("30.00")
        )

    def test_form_page_shows_products(self):
        response = self.client.get("/pos/sale/new/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Fake Coffee")

    def test_valid_sale_redirects_to_detail(self):
        response = self.client.post(
            "/pos/sale/new/",
            {f"qty_{self.coffee.pk}": "2", f"qty_{self.tea.pk}": "0"},
        )
        sale = Sale.objects.get()
        self.assertRedirects(response, f"/pos/sale/{sale.pk}/")
        self.assertEqual(sale.items.count(), 1)

    def test_detail_shows_total(self):
        self.client.post(
            "/pos/sale/new/",
            {f"qty_{self.coffee.pk}": "2", f"qty_{self.tea.pk}": "1"},
        )
        sale = Sale.objects.get()
        response = self.client.get(f"/pos/sale/{sale.pk}/")
        self.assertContains(response, "Total: 130.00")

    def test_no_items_shows_error(self):
        response = self.client.post(
            "/pos/sale/new/",
            {f"qty_{self.coffee.pk}": "0", f"qty_{self.tea.pk}": "0"},
        )
        self.assertContains(response, "Pili ug labing menos usa")
        self.assertEqual(Sale.objects.count(), 0)

    def test_bad_qty_is_ignored(self):
        response = self.client.post(
            "/pos/sale/new/", {f"qty_{self.coffee.pk}": "abc"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Sale.objects.count(), 0)

    def test_missing_sale_returns_404(self):
        response = self.client.get("/pos/sale/9999/")
        self.assertEqual(response.status_code, 404)


class LoginRequiredTest(TestCase):
    def test_products_requires_login(self):
        response = self.client.get("/pos/products/")
        self.assertRedirects(
            response,
            "/accounts/login/?next=/pos/products/",
            fetch_redirect_response=False,
        )

    def test_new_sale_requires_login(self):
        response = self.client.get("/pos/sale/new/")
        self.assertRedirects(
            response,
            "/accounts/login/?next=/pos/sale/new/",
            fetch_redirect_response=False,
        )

    def test_login_page_loads(self):
        response = self.client.get("/accounts/login/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")
