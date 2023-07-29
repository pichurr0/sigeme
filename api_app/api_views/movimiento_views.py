from sigeme_project import logger
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from ..serializer import MovimientoSerializer, MovimientoComponenteSerializer
from ..pagination import CustomPagination
from api_app.models import Movimiento, MovimientoComponente

pagination = CustomPagination()


class ListMovimiento(APIView):
    """
    Listar todos los movimientos de medios

    * Requires token authentication.
    * Only admin users are able to access this view.
    """

    authentication_classes = []
    permission_classes = []

    def get(self, request, pk=None, **kwargs):
        """
        Return a list of all moves.
        """
        logger.info(f'pk: {pk}')
        result = Movimiento.objects.all()

        if pk is not None:
            result = Movimiento.objects.filter(medio=pk)

        serializer = MovimientoSerializer(result, many=True, context={'request': request})

        return Response(serializer.data)


class ListMovimientoComponente(APIView):
    """
    Listar todas las modificacion sobre los componentes

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request, pk=None, **kwargs):
        """
        Return a list of all moves.
        """
        logger.info(f'pk: {pk}')
        result = MovimientoComponente.objects.all()

        if pk is not None:
            result = MovimientoComponente.objects.filter(componente=pk)

        serializer = MovimientoComponenteSerializer(result, many=True, context={'request': request})

        return Response(serializer.data)