from django.test import TestCase
from .factories import ItemFactory
from .serializers import ItemSerializer

class ItemTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.Item = ItemFactory._meta.model

    def test_create(self):
        item = ItemFactory(name='X Item')

        self.assertEqual(item.name, 'X Item')
        self.assertEqual(item.pk, item.id)

    def test_read(self):
        item = ItemFactory(name='X Item')

        self.assertQuerysetEqual(
            self.Item.objects.all(),
            ['<Item: X Item>']
        )

    def test_read(self):
        item = ItemFactory(name='X Item')
        item.name = "Y Item"
        item.save()

        self.assertQuerysetEqual(
            self.Item.objects.all(),
            ['<Item: Y Item>']
        )