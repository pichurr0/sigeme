from django.urls import include, path
from rest_framework import routers
from .views import UserViewSet, ComponenteViewSet, \
    PerifericoViewSet, ComputadoraViewSet, EquipoViewSet
from api_app.api_views.medio_views import ListMedio, ListTipoMedio
# from api_app.api_views.computadora_views import RetrieveDestroyMedio


# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'usuarios', UserViewSet)
router.register(r'componentes', ComponenteViewSet)
router.register(r'perifericos', PerifericoViewSet)
router.register(r'computadoras', ComputadoraViewSet)
router.register(r'equipos', EquipoViewSet)

# Este tipo de router no se muestra en la documentacion de django
simple_router = routers.SimpleRouter()
# simple_router.register(r'perifericos', PerifericoViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    path('', include(router.urls)),
    path('', include(simple_router.urls)),
    path('medios/', ListMedio.as_view(), name='medios'),
    path('tipo_medios/', ListTipoMedio.as_view(), name='tipo_medios'),
    # path('computadoras/<pk>/componentes/<pk_comp>', RetrieveDestroyMedio.as_view(), name='medios'),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
]