from rest_framework import viewsets, permissions, mixins, decorators, response
from .models import Customer, Product, Order
from .serializers import CustomerSerializer, OrdersSerializer, OrdersViewSerializer, OrdersUpdateSerializer, OrdersProductsSerializer, OrdersShipmentSerializer
from .paginators import OrdersPagination


class CreateUpdateListRetrieveViewSet(mixins.CreateModelMixin,
                                      mixins.UpdateModelMixin,
                                      mixins.ListModelMixin,
                                      mixins.RetrieveModelMixin,
                                      viewsets.GenericViewSet):
    pass


class CustomerViewSet(CreateUpdateListRetrieveViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.AllowAny]


class OrdersViewSet(CreateUpdateListRetrieveViewSet):
    queryset = Order.objects.all().order_by('-ordered_at')
    permission_classes = [permissions.AllowAny]
    pagination_class = OrdersPagination

    def get_serializer_class(self):
        if self.action in ["create"]:
            return OrdersSerializer

        if self.action in ["update", "partial_update", "destroy"]:
            return OrdersUpdateSerializer

        return OrdersViewSerializer

    """
        All the requested products in one order
    """
    @decorators.action(methods=['get'], detail=True, permission_classes=[permissions.AllowAny])
    def products(self, request, pk=None):
        products_set = self.queryset.filter(id=pk)
        serializer = OrdersProductsSerializer(products_set, many=True)
        return response.Response(serializer.data)

    """
        All the shipments in one order
    """
    @decorators.action(methods=['get'], detail=True, permission_classes=[permissions.AllowAny])
    def shipments(self, request, pk=None):
        products_set = self.queryset.filter(id=pk)
        serializer = OrdersShipmentSerializer(products_set, many=True)
        return response.Response(serializer.data)

