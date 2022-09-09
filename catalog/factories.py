from factory.django import DjangoModelFactory
from faker import Faker
from .models import Item

faker = Faker()


class ItemFactory(DjangoModelFactory):

    class Meta:
        model = Item
        django_get_or_create = ('name', 'weight', 'stock', 'price')

    name = faker.word()
    weight = faker.pyfloat(left_digits=1, right_digits=2, min_value=0.1, max_value=2)
    stock = faker.random_int(0, 100)
    price = faker.pyfloat(left_digits=3, right_digits=2, min_value=1, max_value=1000)



