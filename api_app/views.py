from datetime import datetime
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
    permission_classes = []



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
    permission_classes = []


class PerifericoViewSet(viewsets.ModelViewSet):
    serializer_class = PerifericoSerializer
    queryset = Periferico.objects.all()
    permission_classes = []
# 77974874

class ComputadoraViewSet(viewsets.ModelViewSet):
    queryset = Computadora.objects.all()
    serializer_class = ComputadoraSerializer
    permission_classes = []

    def create(self, request):
        print('eeee')
        # print(vars(self))
   
        data = request.data
        print('data', data)
        serializer = self.serializer_class(data=data)
        print('serialized---- is valid------')
        print(serializer.is_valid(raise_exception=True))
        if not serializer.is_valid():
            HttpResponse(serializer.errors)
        print('serialized', serializer)
        print(serializer.validated_data)
        entity = serializer.save()
        print('serialized----------', entity)
        entity.save()
        # entity = self.perform_create(serializer)
        # entity = Computadora(
        #     creacion=datetime.now(),
        #     modificacion=datetime.now()
        #     )
        # entity.save()
    
        return HttpResponse('ok')
        # print(vars(request))
        # print(ComputadoraSerializer(request))
        # computadora = Computadora(       
        #     )


def pingView(request):
    return HttpResponse('ping...')    


def testingView(request):
    return render('testing...')    