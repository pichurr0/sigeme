import logging
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status, generics, views
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializer import UserSerializer, MedioSerializer, ComponenteSerializer,\
EquipoSerializer, PerifericoSerializer, ComputadoraSerializer
from .models import Medio, Componente, Equipo, Periferico, Computadora


logger = logging.getLogger(__name__)


class ComponenteViewSet(viewsets.ModelViewSet):
    serializer_class = ComponenteSerializer
    queryset = Componente.objects.all()

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

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


class UserCreate(generics.CreateAPIView):
    serializer_class = UserSerializer


class EquipoViewSet(viewsets.ModelViewSet):
    serializer_class = EquipoSerializer
    queryset = Equipo.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if not serializer.is_valid(raise_exception=True):
            Response(serializer.errors)
        serializer.save()  # retorna la entidad ej: entity=serializer.save() 
        return Response(serializer.data)


class LoginView(views.APIView):
    """
    Gestiona la autenticacion de usuarios a la plataforma via api
    """
    permission_classes = ()
    
    def post(self, request,):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        print('tamos',request.data, user)
        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


def pingView(request):
    return HttpResponse('ping...')    


def testingView(request):
    return render('testing...')    