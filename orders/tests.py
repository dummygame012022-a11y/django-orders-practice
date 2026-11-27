from django.test import TestCase

# Create your tests here.

from django.contrib.auth.models import User

from .models import Order


class OrderListTest(TestCase):
    def setUp(self):
        self.client.force_login(User.objects.create_user("fakecashier"))

    def test_list_shows_order(self):
        Order.objects.create(order="T001", item="Fake", qty=3)
        response = self.client.get("/orders/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "T001 - Fake x3")

    def test_list_empty(self):
        response = self.client.get("/orders/")
        self.assertContains(response, "Walay order pa.")


class OrderCrudTest(TestCase):
    def setUp(self):
        self.client.force_login(User.objects.create_user("fakecashier"))

    def test_add_order(self):
        response = self.client.post(
            "/orders/add/", {"order": "T002", "item": "Fake", "qty": 2}
        )
        self.assertRedirects(response, "/orders/")
        self.assertTrue(Order.objects.filter(order="T002").exists())

    def test_edit_order(self):
        o = Order.objects.create(order="T001", item="Fake", qty=3)
        response = self.client.post(
            f"/orders/{o.pk}/edit/", {"order": "T001", "item": "Fake", "qty": 5}
        )
        self.assertRedirects(response, "/orders/")
        o.refresh_from_db()
        self.assertEqual(o.qty, 5)

    def test_delete_confirm_page(self):
        o = Order.objects.create(order="T001", item="Fake", qty=3)
        response = self.client.get(f"/orders/{o.pk}/delete/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Order.objects.filter(pk=o.pk).exists())

    def test_delete_order(self):
        o = Order.objects.create(order="T001", item="Fake", qty=3)
        response = self.client.post(f"/orders/{o.pk}/delete/")
        self.assertRedirects(response, "/orders/")
        self.assertFalse(Order.objects.filter(pk=o.pk).exists())

    def test_edit_missing_returns_404(self):
        response = self.client.get("/orders/9999/edit/")
        self.assertEqual(response.status_code, 404)


class OrdersLoginRequiredTest(TestCase):
    def test_list_requires_login(self):
        response = self.client.get("/orders/")
        self.assertRedirects(
            response,
            "/accounts/login/?next=/orders/",
            fetch_redirect_response=False,
        )

    def test_add_requires_login(self):
        response = self.client.get("/orders/add/")
        self.assertRedirects(
            response,
            "/accounts/login/?next=/orders/add/",
            fetch_redirect_response=False,
        )
