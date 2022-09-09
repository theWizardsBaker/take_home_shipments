from rest_framework import viewsets, permissions, mixins

from .models import Item
from .serializers import ItemSerializer


class CreateUpdateListRetrieveViewSet(mixins.CreateModelMixin,
                                      mixins.UpdateModelMixin,
                                      mixins.ListModelMixin,
                                      mixins.RetrieveModelMixin,
                                      viewsets.GenericViewSet):
    pass


class ItemViewSet(CreateUpdateListRetrieveViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.AllowAny]
