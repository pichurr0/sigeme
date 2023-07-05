from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework import serializers
from .nomenclators import TipoMedio, TipoMarca, TipoModelo,TipoEstadoMedio, TipoEstadoSello
from .models import Medio, Componente, Equipo, Periferico, Computadora, Ubicacion

from sigeme_project import logger
# Serializers define the API representation.


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Serializaror de Usuarios.

       Este modelo en la api tendra un atributo url en el que se podran ver todos los detalles del mismo
    """

    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


class NomencladorSerializer(serializers.Serializer):
    """Componentes que van dentro de una computadora."""

    id = serializers.IntegerField(label='ID')
    tipo = serializers.CharField()


class ValueLabelSerializer(serializers.Serializer):
    """Serializador para datos que no tienen una representacion en forma de modelo."""

    value = serializers.CharField()
    label = serializers.CharField()


class MarcaSerializer(NomencladorSerializer, serializers.ModelSerializer):
    """Serializador para datos que no tienen una representacion en forma de modelo."""

    class Meta:
        model = TipoMarca
        fields = '__all__'
    
    def create(self, validated_data):
        print('marca serializer')


class EstadoSelloSerializer(NomencladorSerializer, serializers.ModelSerializer):
    """Serializador para datos que no tienen una representacion en forma de modelo."""

    class Meta:
        model = TipoEstadoSello
        fields = '__all__'
    
    def create(self, validated_data):
        print('sello serializer')


class EstadoMedioSerializer(NomencladorSerializer, serializers.ModelSerializer):
    """Serializador para datos que no tienen una representacion en forma de modelo."""

    class Meta:
        model = TipoEstadoMedio
        fields = '__all__'
    
    def create(self, validated_data):
        print('estado serializer')


class ModeloSerializer(NomencladorSerializer, serializers.ModelSerializer):
    """Serializador para datos que no tienen una representacion en forma de modelo."""
    
    marca = serializers.IntegerField(label='ID', read_only=True)

    class Meta:
        model = TipoModelo
        fields = '__all__'
    
    def create(self, validated_data):
        print('modelo serializer')


class UbicacionSerializer(serializers.ModelSerializer):
    """Serializador de Ubicacion."""
   
    id = serializers.IntegerField(label='ID')
    division = NomencladorSerializer(read_only=True)
    municipio = NomencladorSerializer(read_only=True)
    unidad = NomencladorSerializer(read_only=True)
    departamento = NomencladorSerializer(read_only=True)

    class Meta:
        model = Ubicacion
        exclude = ['text']


class TipoMedioSerializer(serializers.ModelSerializer):
    """Serializador de TipoMedio."""

    # foto = serializers.ImageField(blank=True,null=True)
    tipo = serializers.StringRelatedField()

    class Meta:
        model = TipoMedio
        exclude = ['slug']


# Serializador padre para todas los hijos de medio basico
# class MedioSerializer(serializers.ModelSerializer):
class MedioSerializer(serializers.Serializer):
    """Serializador de Medio.

    Ni convirtiendo esta clase a Serializer se pueden solicitar atributos
    de las clases hijas. Dichos attrs no se encuentran en la clase medio.
    """

    # fixme, me quede intentando de representar las relaciones entre modelos de una forma mas amigable
    # foto = serializers.ImageField(blank=True,null=True)
    tipo = serializers.CharField()
    serie = serializers.CharField()
    # marca = serializers.CharField()
    # marca = NomencladorSerializer()
    marca = MarcaSerializer()
    modelo = ModeloSerializer()
    estado = EstadoMedioSerializer()
    ubicacion = UbicacionSerializer()
    creacion = serializers.DateTimeField(
        default=serializers.CreateOnlyDefault(timezone.now)
    )
    modificacion = serializers.DateTimeField(
        read_only=True,
        default=datetime.now()
    )

    class Meta:
        model = Medio
        fields = ['id', 'tipo', 'serie', 'marca', 'modelo', 'estado', 'ubicacion']
        read_only_fields = ['creacion', 'modificacion']
        depth = 1  # revisar denuevo esto para que es


class ComponenteSerializer(MedioSerializer, serializers.ModelSerializer):
    """Componentes que van dentro de una computadora."""

    tipo_componente = serializers.CharField()
    tipo_ram = serializers.CharField()
    tipo_capacidad = serializers.CharField()
    tipo_frecuencia = serializers.CharField()

    class Meta:
        model = Componente
        fields = '__all__'


class EquipoSerializer(MedioSerializer, serializers.ModelSerializer):
    """Componentes que van dentro de una computadora."""

    inventario = serializers.CharField()

    class Meta:
        model = Equipo
        fields = '__all__'


class PerifericoSerializer(MedioSerializer,serializers.ModelSerializer):
    """Equipos que son perifericos a la computadora."""

    conectado_a = serializers.CharField()
    tipo_periferico = serializers.CharField()

    class Meta:
        model = Periferico
        fields = '__all__'


class ComputadoraSerializer(MedioSerializer, serializers.ModelSerializer):
    """Componentes que van dentro de una computadora."""

    sello = serializers.CharField()
    estado_sello = NomencladorSerializer()

    class Meta:
        model = Computadora
        fields = '__all__'

    def create(self, validated_data):
        """
        Fue necesario sobrescribir este metodo
        """

        print('en el serializer.py')
        # logger.info(f'dentro de serialize {validated_data}')

        # computadora = Computadora()
        data = validated_data
        marca = TipoMarca.objects.filter(id=validated_data['marca']['id']).first()
        if marca:
            data['marca'] = marca

        modelo = TipoModelo.objects.filter(id=validated_data['modelo']['id']).first()
        if modelo:
            data['modelo'] = modelo

        estado = TipoEstadoMedio.objects.filter(id=validated_data['estado']['id']).first()
        if estado:
            data['estado'] = estado

        ubicacion = Ubicacion.objects.filter(id=validated_data['ubicacion']['id']).first()
        if ubicacion:
            data['ubicacion'] = ubicacion

        estado_sello = TipoEstadoSello.objects.filter(id=validated_data['estado_sello']['id']).first()
        if estado_sello:
            data['estado_sello'] = estado_sello

        return Computadora.objects.create(**data)
