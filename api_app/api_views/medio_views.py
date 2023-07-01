from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from ..serializer import MedioSerializer, ComputadoraSerializer, EquipoSerializer, PerifericoSerializer
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


    def get(self, request):
        """
        Return a list of all users.
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

                query3 = Computadora.objects.filter(Q(ip__icontains=search) |
                Q(servicio__icontains=search))\
                .values("id")  # noqa: E122

                # union de todos los tipos de medios
                identifiers = query1.union(query2).union(query3)
                print('identifiers',identifiers)

                # queryset = queryset.filter(Q(serie__icontains=search))

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
        result_page = paginator.paginate_queryset(queryset, request)

        serializer = MedioSerializer(result_page, many=True, context={'request': request})
        response = paginator.get_paginated_response(serializer.data)

        return response

    def post(self, request, tipo=None):
        pass


class RetrieveDestroyMedio(RetrieveUpdateDestroyAPIView):
    """
    Manage the crud operation get and delete over medios model
    """
    authentication_classes = []
    permission_classes = []
    # queryset = Medio.objects.all()
    # serializer_class = MedioSerializer
    lookup_field = 'id'

    def retrieve(self, request, pk=None, *args, **kwargs):

        queryset = self.get_queryset().filter(id=pk).first()
        if queryset.tipo == TipoMedio.COMPUTADORA:
            queryset = Computadora(queryset)
            serialized = ComputadoraSerializer(queryset, many=False, context={'request': request})
        elif queryset.tipo == TipoMedio.EQUIPO:
            serialized = ComputadoraSerializer(queryset, many=False, context={'request': request})
        elif queryset.tipo == TipoMedio.PERIFERICO:
            serialized = ComputadoraSerializer(queryset, many=False, context={'request': request})
        else:
            serialized = MedioSerializer(queryset, many=False, context={'request': request})

        return Response(serialized.data,  status=status.HTTP_200_OK)

    # def get(self, request, pk=None):
    #     print(pk)
    #     queryset = Medio.objects.filter(id=pk)
    #     MedioSerializer(queryset, many=False, context={'request': request})

    def destroy(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset().filter(id=pk).first()
        # queryset.
        return Response({"msg": "deleted"},  status=status.HTTP_200_OK)


# class ManageMedio(RetrieveDestroyAPIView):

#     def update(self, request, pk=None):
#         pass
