from rest_framework import serializers
from .models import Shipment, ShipmentProduct


class ShipmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shipment
        fields = [
            'order',
            'has_shipped',
            'shipping_date',
            'shipping_products',
            'shipping_weight',
        ]


class ShipmentUpdateSerializer(serializers.ModelSerializer):

    class Meta(ShipmentSerializer.Meta):
        read_only_fields = ['order']


class ShipmentProductsSerializer(serializers.ModelSerializer):

    from orders.serializers import ProductSerializer

    product = ProductSerializer()

    class Meta:
        model = ShipmentProduct
        fields = ['id', 'quantity', 'product']


class ProductListSerializer(serializers.ModelSerializer):

    # from orders.serializers import ProductSerializer
    from catalog.serializers import ItemSerializer

    item = ItemSerializer()

    class Meta:
        model = ShipmentProduct
        fields = ['id', 'quantity', 'item']


class ShipmentViewSerializer(serializers.ModelSerializer):
    shipping_address = serializers.CharField(source="order.customer.shipping_address")
    order_fulfilled = serializers.BooleanField(source="order.is_fulfilled")
    shipping_products = ProductListSerializer(many=True)

    class Meta:
        model = Shipment
        fields = [
            'has_shipped',
            'order',
            'order_fulfilled',
            'shipping_address',
            'shipping_date',
            'shipping_products',
            'shipping_weight',
        ]
        depth = 1


class ShipmentProductViewSerializer(serializers.ModelSerializer):
    shipping_address = serializers.CharField(source="order.customer.shipping_address")

    class Meta:
        model = Shipment
        fields = [
            'id',
            'has_shipped',
            'shipping_address',
            'shipping_date',
            'shipping_products',
            'shipping_weight',
        ]
        depth = 1

