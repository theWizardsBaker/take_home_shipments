from factory.django import DjangoModelFactory
from faker import Faker
from .models import Shipment

from orders.factories import OrderFactory

faker = Faker()


class ShipmentFactory(DjangoModelFactory):

    class Meta:
        model = Shipment
        django_get_or_create = ('order', 'has_shipped', 'shipping_weight', 'shipping_date')

    order = None
    has_shipped = False
    shipping_weight = faker.random_int(1, 2)
    shipping_date = faker.date()


