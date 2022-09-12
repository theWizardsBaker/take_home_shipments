from rest_framework import viewsets, permissions, mixins, response, decorators
from .models import Shipment, ShipmentProduct
from .serializers import ShipmentSerializer, ShipmentUpdateSerializer, ShipmentViewSerializer, ShipmentProductsSerializer


class CreateUpdateListRetrieveViewSet(mixins.CreateModelMixin,
                                      mixins.UpdateModelMixin,
                                      mixins.ListModelMixin,
                                      mixins.RetrieveModelMixin,
                                      viewsets.GenericViewSet):
    pass


class ShipmentViewSet(CreateUpdateListRetrieveViewSet):
    queryset = Shipment.objects.all()
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action in ["create"]:
            return ShipmentSerializer

        if self.action in ["update", "partial_update", "destroy"]:
            return ShipmentUpdateSerializer

        return ShipmentViewSerializer

    """
        All the products in a single package
    """
    @decorators.action(methods=['get'], detail=True, permission_classes=[permissions.AllowAny])
    def packaged_products(self, request, pk=None):
        shipment = self.queryset.filter(id=pk)
        shipment_products = ShipmentProduct.objects.filter(shipment=shipment[0])
        serializer = ShipmentProductsSerializer(shipment_products, many=True)
        return response.Response(serializer.data)

