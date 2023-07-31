from sigeme_project import logger
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from ..serializer import MedioSerializer
from ..pagination import CustomPagination
from ..nomenclators import TipoMedio
from api_app.models import Medio, Equipo, Periferico, Computadora

pagination = CustomPagination()


class ListarMedio(APIView):
    """
    Listar los medios del sistema

    * Requires token authentication.
    * Only admin users are able to access this view.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        obtener todos los medios
        """

        search = request.query_params.get('search')
        tipo = request.query_params.get('tipo')
        searching = search is not None
        identifiers = []

        if tipo is None:
            queryset = Medio.objects.all()

            if searching:

                # queryset = Medio.objects.all()
                query1 = Periferico.objects.filter(
                    Q(serie__icontains=search) |
                    Q(tipo_periferico__tipo__icontains=search)) \
                .values_list("id")  # noqa: E122

                query2 = Equipo.objects.filter(inventario__icontains=search)\
                .values("id")  # noqa: E122

                query3 = Computadora.objects.filter(
                    Q(ip__icontains=search)
                    | Q(servicio__icontains=search))\
                .values("id")  # noqa: E122

                # union de todos los tipos de medios
                identifiers = query1.union(query2).union(query3)

        elif tipo is not None and tipo in TipoMedio.values:
            
            queryset = Medio.objects.filter(tipo=tipo)

            if searching:
                
                if tipo == TipoMedio.COMPUTADORA:
                    identifiers = Computadora.objects.filter(
                        Q(ip__icontains=search)
                        | Q(servicio__icontains=search))
                elif tipo == TipoMedio.EQUIPO:
                    identifiers = Equipo.objects.filter(inventario__icontains=search)
                elif tipo == TipoMedio.PERIFERICO:
                    identifiers = Periferico.objects.filter(
                    Q(serie__icontains=search)
                    | Q(tipo_periferico__tipo__icontains=search))
                    
        else:
            queryset = []

        # this is not optime but i wanna test how look like with inheritance
        if searching:
            queryset = Medio.objects.filter(
                Q(
                    Q(id__in=identifiers)
                )
                &
                Q(tipo__icontains=search)
                | Q(serie__icontains=search)
                | Q(marca__tipo__icontains=search)
                | Q(modelo__tipo__icontains=search)
                | Q(estado__tipo__icontains=search)
                | Q(ubicacion__text__icontains=search)
                )

        if not tipo is None:
            queryset = queryset.filter(tipo=tipo)

        # ordenar
        queryset = queryset.order_by("-id")

        paginator = CustomPagination()
        # logger.info('tremendoSS', queryset)
        result_page = paginator.paginate_queryset(queryset, request)

        serializer = MedioSerializer(result_page, many=True, context={'request': request})
        response = paginator.get_paginated_response(serializer.data)

        return response