from django.test import TestCase

# Create your tests here.

from .models import Order


class OrderListTest(TestCase):
    def test_list_shows_order(self):
        Order.objects.create(order="T001", item="Fake", qty=3)
        response = self.client.get("/orders/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "T001 - Fake x3")

    def test_list_empty(self):
        response = self.client.get("/orders/")
        self.assertContains(response, "Walay order pa.")
