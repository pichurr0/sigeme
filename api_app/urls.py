from django.urls import include, path
from rest_framework import routers
from .views import UserViewSet, MedioViewSet, ComponenteViewSet, \
      PerifericoViewSet, ComputadoraViewSet, EquipoViewSet
from api_app.api_views.medio_views import ListMedio


# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'usuarios', UserViewSet)
router.register(r'componentes', ComponenteViewSet)
router.register(r'mediosset', MedioViewSet)

# Este tipo de router no se muestra en la documentacion de django
simple_router = routers.SimpleRouter()
simple_router.register(r'perifericos', PerifericoViewSet)
simple_router.register(r'computadoras', ComputadoraViewSet)
simple_router.register(r'equipos', EquipoViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    path('', include(router.urls)),
    path('', include(simple_router.urls)),
    path('medios/', ListMedio.as_view(), name='medios'),
    path('medios/<tipo>/', ListMedio.as_view(), name='medios'),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
]