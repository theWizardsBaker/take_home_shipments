from factory.django import DjangoModelFactory
from faker import Faker

from .models import Customer, Order

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


class OrderFactory(DjangoModelFactory):
    customer = CustomerFactory()
    ordered_at = faker.date()
    is_fulfilled = False

    class Meta:
        model = Order