from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializer import MedioSerializer
from ..pagination import CustomPagination
from ..nomenclators import TipoMedio

from api_app.models import Medio, Componente, Equipo, Periferico, Computadora

pagination = CustomPagination()


class ListMedio(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """

    authentication_classes = []
    permission_classes = []


    def get(self, request, tipo=None):
        """
        Return a list of all users.
        """

        search = request.query_params.get('search')
        searching = search is not None

        if tipo is None:
            queryset = Medio.objects.all()

            if searching:

                # queryset = Medio.objects.all()
                query1 = Periferico.objects.filter(
                    Q(tipo_periferico__tipo__icontains=search)) \
                .values("id", "tipo", "marca", "modelo", "estado")  # noqa: E122

                query2 = Equipo.objects.filter(inventario__icontains=search)\
                .values("id", "tipo", "marca", "modelo", "estado")  # noqa: E122

                query3 = Computadora.objects.filter(Q(ip__icontains=search) |
                Q(servicio__icontains=search))\
                .values("id", "tipo", "marca", "modelo", "estado")  # noqa: E122

                # union de todos los tipos de medios
                queryset = query1.union(query2).union(query3)

                queryset = queryset.filter(Q(serie__icontains=search))

            # ordenar 
            queryset = queryset.order_by("-id")  # .values()

        elif tipo is not None and tipo in TipoMedio.values:
            queryset = Medio.objects(Q(tipo=tipo)).all()

            if searching:
            	pass

        else:
            queryset = []

        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(queryset, request)

        if not searching:
            serializer = MedioSerializer(result_page, many=True, context={'request': request})
            response = paginator.get_paginated_response(serializer.data)
        else:
            response = paginator.get_paginated_response(queryset)

        return response
