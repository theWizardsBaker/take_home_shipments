from django.db import models
from orders.models import Order, Product


class Shipment(models.Model):
    """
        A single shipment (container)
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    has_shipped = models.BooleanField(default=False, db_index=True)
    shipping_weight = models.PositiveSmallIntegerField(default=0)
    shipping_date = models.DateTimeField()
    """
        Multiple products can be included in one shipment
    """
    shipping_products = models.ManyToManyField(
        Product,
        through='ShipmentProduct',
    )

    def __str__(self):
        return f"Shipment: {self.id} @ {self.shipping_date}"


class ShipmentProduct(models.Model):
    quantity = models.PositiveSmallIntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.quantity} - {self.product}"
