from enum import unique
from django.db import models
from django.core.validators import MinValueValidator
from catalog.models import Item


class Customer(models.Model):
    fname = models.CharField(max_length=100, verbose_name="First Name")
    lname = models.CharField(max_length=100, verbose_name="Last Name")
    address_1 = models.CharField(max_length=100)
    address_2 = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.fname} {self.lname}"

    @property
    def shipping_address(self):
        return "\n".join([
            f"{self.address_1} {self.address_2}",
            f"{self.city}, {self.state}",
            self.zip
        ])

    @property
    def full_name(self):
        return f"{self.fname} {self.lname}"


class Order(models.Model):
    customer = models.ForeignKey(
        "Customer",
        on_delete=models.CASCADE,
    )
    ordered_at = models.DateTimeField(auto_created=True)
    is_fulfilled = models.BooleanField(db_index=True)

    def __str__(self):
        return f"{self.products.count()} items - {self.ordered_at} - {self.customer}"


class Product(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='products'
    )
    quantity = models.PositiveSmallIntegerField(
        default=0,
        validators=[
            MinValueValidator(0, message="quantity must be at least 1"),
        ],
        blank=False
    )

    class Meta:
        # an item in an order must be unique
        unique_together = ('item', 'order',)

    def __str__(self):
        return f"Product ordered: {self.quantity} of \"{self.item}\""


