from django.db import models
from django.core.validators import MinValueValidator


class Item(models.Model):
    name = models.CharField(
        help_text="Product name",
        max_length=200
    )
    weight = models.DecimalField(
        help_text="1-2 (lbs)",
        decimal_places=2,
        max_digits=3,
        validators=[
            MinValueValidator(0, message="Cannot have zero weight"),
        ]
    )
    stock = models.PositiveSmallIntegerField(
        help_text="Current supply",
        default=0
    )
    price = models.DecimalField(
        help_text="Mark up price",
        decimal_places=2,
        max_digits=10
    )

    def __str__(self):
        return f"{self.name}"