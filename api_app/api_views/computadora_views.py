from sigeme_project import logger
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from ..serializer import ComponenteSerializer
from ..pagination import CustomPagination
from ..nomenclators import TipoMedio
from ..views import ComponenteViewSet
from api_app.models import Medio, Componente, Equipo, Periferico, Computadora

pagination = CustomPagination()


class ListComponentesComputadora(APIView):
    """
    Listar todos los componentes de una computadora

    * Requires token authentication.
    * Only admin users are able to access this view.
    """

    authentication_classes = []
    permission_classes = []

    def get(self, request, pk, **kwargs):
        """
        Return a list of all users.
        """
        result = Componente.objects.filter(medio=pk)

        serializer = ComponenteSerializer(result, many=True, context={'request': request})

        return Response(serializer.data)

    def post(self, request, pk=None, **kwargs):

        data = request.data
        data['medio'] = pk
        serializer = ComponenteSerializer(data=data)
        if not serializer.is_valid(raise_exception=True):
            return Response(serializer.errors)
        serializer.save()  # retorna la entidad ej: entity=serializer.save() 
        return Response(serializer.data)


class RetrieveDestroyComponenteComputadora(RetrieveUpdateDestroyAPIView):
    """
    Obtener Actualizar y Eliminar Componente de computadora
    """
    queryset = Componente.objects.all()
    serializer_class = ComponenteSerializer

    def get(self, request, pk=None, pk_comp=None, **kwargs):
        """
        self.get_object() lanza excepcion porque no existe un componente con pk de computadora
        """
        logger.info('obteniendo componentet de computadora')
        try:
            instance = self.queryset.filter(Q(medio__id=pk) & Q(id=pk_comp)).first()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Exception as err:
            print('error', err )
            return Response(str(err))

    def put(self, request, pk=None, pk_comp=None, *args, **kwargs):
        return ComponenteViewSet.update(request, pk=pk_comp, *args, **kwargs)

    def delete(self, request, pk=None, pk_comp=None, *args, **kwargs):
        instance = self.queryset.filter(Q(medio__id=pk) & Q(id=pk_comp)).first()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



