from django.contrib.auth import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('orders.urls')),
    path('api/', include('shipments.urls')),
    path('api/', include('catalog.urls'))
]


if settings.DEBUG:
    from django.conf.urls import url
    from rest_framework import permissions
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi

    schema_view = get_schema_view(
       openapi.Info(
          title="Sundjango API",
          default_version='v1',
          description="The API that helps you grow!",
       ),
       public=False,
       permission_classes=(permissions.AllowAny,),
    )

    urlpatterns += [
       url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    ]
