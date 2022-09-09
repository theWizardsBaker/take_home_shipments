from rest_framework.routers import SimpleRouter
from .views import CustomerViewSet, OrdersViewSet

router = SimpleRouter()
router.register("customers", CustomerViewSet)
router.register("orders", OrdersViewSet)

urlpatterns = router.urls
