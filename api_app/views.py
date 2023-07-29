import logging
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializer import UserSerializer, MedioSerializer, ComponenteSerializer,\
EquipoSerializer, PerifericoSerializer, ComputadoraSerializer
from .models import Medio, Componente, Equipo, Periferico, Computadora



logger = logging.getLogger(__name__)


class ComponenteViewSet(viewsets.ModelViewSet):
    serializer_class = ComponenteSerializer
    queryset = Componente.objects.all()
    permission_classes = []

    def create(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if not serializer.is_valid(raise_exception=True):
            Response(serializer.errors)
        serializer.save()  # retorna la entidad ej: entity=serializer.save() 
        return Response(serializer.data)

    def update(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid(raise_exception=True):
            return Response(serializer.errors)
        # Persistiendo en base de datos
        serializer.save()

        #hacer movimiento

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class EquipoViewSet(viewsets.ModelViewSet):
    serializer_class = EquipoSerializer
    queryset = Equipo.objects.all()
    permission_classes = []

    def create(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if not serializer.is_valid(raise_exception=True):
            Response(serializer.errors)
        serializer.save()  # retorna la entidad ej: entity=serializer.save() 
        return Response(serializer.data)

    def update(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid(raise_exception=True):
            return Response(serializer.errors)
        # Persistiendo en base de datos
        serializer.save()
        return Response(serializer.data)


class PerifericoViewSet(viewsets.ModelViewSet):
    serializer_class = PerifericoSerializer
    queryset = Periferico.objects.all()
    permission_classes = []

    def create(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if not serializer.is_valid(raise_exception=True):
            Response(serializer.errors)
        serializer.save()  # retorna la entidad ej: entity=serializer.save() 
        return Response(serializer.data)

    def update(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid(raise_exception=True):
            return Response(serializer.errors)
        # Persistiendo en base de datos
        serializer.save()
        return Response(serializer.data)

class ComputadoraViewSet(viewsets.ModelViewSet):
    serializer_class = ComputadoraSerializer
    queryset = Computadora.objects.all()
    permission_classes = []

    def create(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if not serializer.is_valid(raise_exception=True):
            Response(serializer.errors)
        serializer.save()  # retorna la entidad ej: entity=serializer.save() 
        return Response(serializer.data)


class MedioViewSet(viewsets.ModelViewSet):
    serializer_class = MedioSerializer
    queryset = Medio.objects.all()
    lookup_field = 'tipo'

    @action(methods=['get'], detail=False, permission_classes=[],
            url_path='', url_name='medios-list')
    def get_all(self, request, pk='id'):
        print('eeee')
        print(request)
        exit()


def pingView(request):
    return HttpResponse('ping...')    


def testingView(request):
    return render('testing...')    