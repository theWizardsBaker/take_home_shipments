from django.contrib import admin
from .models import Shipment, ShipmentProduct


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    class Meta:
        model = Shipment


@admin.register(ShipmentProduct)
class ShipmentProductAdmin(admin.ModelAdmin):
    class Meta:
        model = ShipmentProduct
