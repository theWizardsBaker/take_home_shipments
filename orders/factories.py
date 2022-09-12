from factory.django import DjangoModelFactory
from faker import Faker

from .models import Customer, Order
from catalog.factories import ItemFactory

faker = Faker()


class CustomerFactory(DjangoModelFactory):
    fname = faker.first_name()
    lname = faker.last_name()
    address_1 = faker.street_address()
    address_2 = faker.street_suffix()
    city = faker.city()
    state = faker.state()
    zip = faker.postcode()

    class Meta:
        model = Customer
        django_get_or_create = ('fname', 'lname', 'address_1', 'address_2', 'city', 'state', 'zip',)


class OrderFactory(DjangoModelFactory):
    customer = CustomerFactory()
    ordered_at = faker.date()
    is_fulfilled = False

    class Meta:
        model = Order
        django_get_or_create = ('customer', 'ordered_at', 'is_fulfilled',)


class ProductFactory(DjangoModelFactory):
    item = ItemFactory()
    order = OrderFactory()
    quantity = faker.random_int(1, 12)

    class Meta:
        model = Order
        django_get_or_create = ('item', 'order', 'quantity',)
