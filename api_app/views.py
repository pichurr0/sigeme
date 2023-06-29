from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView

from .serializer import UserSerializer, MedioSerializer, ComponenteSerializer,\
EquipoSerializer, PerifericoSerializer, ComputadoraSerializer
from .models import Medio, Componente, Equipo, Periferico, Computadora


class ComponenteViewSet(viewsets.ModelViewSet):
    serializer_class = ComponenteSerializer
    queryset = Componente.objects.all()


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


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


class EquipoViewSet(viewsets.ModelViewSet):
    serializer_class = EquipoSerializer
    queryset = Equipo.objects.all()


class PerifericoViewSet(viewsets.ModelViewSet):
    serializer_class = PerifericoSerializer
    queryset = Periferico.objects.all()


class ComputadoraViewSet(viewsets.ModelViewSet):
    serializer_class = ComputadoraSerializer
    queryset = Computadora.objects.all()


def pingView(request):
    return HttpResponse('ping...')    


def testingView(request):
    return render('testing...')    