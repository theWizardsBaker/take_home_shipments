from rest_framework import serializers
from .models import Customer, Order, Product
from catalog.serializers import ItemSerializer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['fname', 'lname', 'address_1', 'address_2', 'city', 'state', 'zip']


class ProductSerializer(serializers.ModelSerializer):

    item = ItemSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['quantity', 'item']
        read_only_fields = ['item', 'order']


class OrdersSerializer(serializers.ModelSerializer):

    products = ProductSerializer(read_only=True, many=True)

    class Meta:
        model = Order
        fields = ['customer', 'products', 'ordered_at', 'is_fulfilled']


class OrdersUpdateSerializer(serializers.ModelSerializer):

    class Meta(OrdersSerializer.Meta):
        read_only_fields = ['customer', 'ordered_at']


class OrdersViewSerializer(serializers.ModelSerializer):

    class Meta(OrdersSerializer.Meta):
        # easy way to show the relations
        depth = 1


class OrdersProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'products']
        depth = 1


class OrdersShipmentSerializer(serializers.ModelSerializer):

    from shipments.serializers import ShipmentProductViewSerializer

    shipments = ShipmentProductViewSerializer(source="shipment_set", many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['ordered_at', 'is_fulfilled', 'shipments']
        depth = 1
