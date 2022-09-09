from rest_framework.routers import SimpleRouter
from .views import ShipmentViewSet
from django.urls import path

router = SimpleRouter()
router.register("shipments", ShipmentViewSet)

urlpatterns = router.urls
