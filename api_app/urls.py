from django.urls import include, path
from rest_framework import routers
from .views import ComponenteViewSet, \
    PerifericoViewSet, ComputadoraViewSet, EquipoViewSet, LoginView, UserCreate
from api_app.api_views.medio_views import ListarMedio
from api_app.api_views.nomenclador_views import ListTipoMedio, ListTipoRam, \
     ListTipoEstadoMedio, ListTipoComponente, ListTipoEstadoSello
from api_app.api_views.computadora_views import ListComponentesComputadora, \
     RetrieveDestroyComponenteComputadora
from api_app.api_views.movimiento_views import ListMovimiento, ListMovimientoComponente

# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'componentes', ComponenteViewSet)
router.register(r'perifericos', PerifericoViewSet)
router.register(r'computadoras', ComputadoraViewSet)
router.register(r'equipos', EquipoViewSet)

# Este tipo de router no se muestra en la documentacion de django
# registra rutas igual que default router
simple_router = routers.SimpleRouter()

urlpatterns = [
    path('', include(router.urls)),
    # path('', include(simple_router.urls)),
    path('medios/', ListarMedio.as_view(), name='medios'),
    path('tipo_medios/', ListTipoMedio.as_view(), name='tipo_medios'),
    path('tipo_estado_medios/', ListTipoEstadoMedio.as_view(), name='tipo_estado_medios'),
    path('tipo_estado_sellos/', ListTipoEstadoSello.as_view(), name='tipo_estado_sellos'),
    path('tipo_componentes/', ListTipoComponente.as_view(), name='tipo_componentes'),
    path('tipo_rams/', ListTipoRam.as_view(), name='tipo_rams'),
    path('computadoras/<pk>/componentes/', ListComponentesComputadora.as_view(), name='listar_componentes'),
    path('computadoras/<pk>/componentes/<pk_comp>/', RetrieveDestroyComponenteComputadora.as_view(), name='gestion_componentes'),
    path('movimientos/', ListMovimiento.as_view(), name='movimientos'),
    path('movimientos/<pk>/', ListMovimiento.as_view(), name='movimientos'),
    path('movimientos_componentes/', ListMovimientoComponente.as_view(), name='movimientos_componentes'),
    path('movimientos_componentes/<pk>/', ListMovimientoComponente.as_view(), name='movimientos_componentes'),
    path("login/", LoginView.as_view(), name="login_api"),
    path("users/", UserCreate.as_view(), name="user_create"),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
]