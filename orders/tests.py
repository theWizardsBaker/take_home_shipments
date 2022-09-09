from django.test import TestCase

from .factories import CustomerFactory, OrderFactory


class CustomerTestCase(TestCase):

    def test_creation(self):
        customer = CustomerFactory()
        self.assertEqual(f"{customer.fname} {customer.lname}", str(customer))


class ObjectTestCase(TestCase):

    def test_creation(self):
        order = OrderFactory(customer=CustomerFactory())
        self.assertEqual(order.is_fulfilled, False)
