from django.test import TestCase
from datetime import datetime

from shipments.factories import ShipmentFactory

from orders.factories import OrderFactory, CustomerFactory


class ShipmentTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.Shipment = ShipmentFactory._meta.model

    def test_creation(self):
        ship = ShipmentFactory(order=OrderFactory(customer=CustomerFactory()), has_shipped=True)
        self.assertEqual(ship.pk, ship.id)
        self.assertEqual(ship.has_shipped, True)

    def test_read(self):
        ship = ShipmentFactory(
            order=OrderFactory(customer=CustomerFactory()),
            has_shipped=False
        )

        self.assertQuerysetEqual(
            self.Shipment.objects.all(),
            [f"<Shipment: Shipment: {ship.id}>"]
        )

    def test_write(self):
        ship = ShipmentFactory(
            order=OrderFactory(customer=CustomerFactory()),
            has_shipped=False
        )

        self.assertEqual(ship.has_shipped, False)
        ship.has_shipped = True
        ship.save()

        self.assertEqual(ship.has_shipped, True)

