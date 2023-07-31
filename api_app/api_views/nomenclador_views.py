from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..nomenclators import TipoMedio, TipoEstadoMedio, \
     TipoComponente, TipoRam, TipoEstadoSello


class ListTipoMedio(APIView):
    """
    Listar todos los tipos de medios del sistema

    * No Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = ()
    permission_classes = ()

    def get(self, request):
        data = [{"value": tipo[0], "label":tipo[1]} for tipo in TipoMedio.choices]
        response = Response(data, status.HTTP_200_OK)
        return response


class ListTipoEstadoMedio(APIView):
    """
    Listar los estados del medio

    * No Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = ()
    permission_classes = ()

    def get(self, request):
        data = [{"value": tipo[0], "label":tipo[1]} for tipo in TipoEstadoMedio.choices]
        response = Response(data, status.HTTP_200_OK)
        return response


class ListTipoComponente(APIView):
    """
    Listar los tipos de componentes

    * No Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = ()
    permission_classes = ()

    def get(self, request):
        data = [{"value": tipo[0], "label":tipo[1]} for tipo in TipoComponente.choices]
        response = Response(data, status.HTTP_200_OK)
        return response


class ListTipoRam(APIView):
    """
    Listar los tipos de ram

    * No Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        data = [{"value": tipo[0], "label":tipo[1]} for tipo in TipoRam.choices]
        response = Response(data, status.HTTP_200_OK)
        return response


class ListTipoEstadoSello(APIView):
    """
    Listar los tipos de ram

    * No Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = ()
    permission_classes = ()

    def get(self, request):
        data = [{"value": tipo[0], "label":tipo[1]} for tipo in TipoEstadoSello.choices]
        response = Response(data, status.HTTP_200_OK)
        return response
