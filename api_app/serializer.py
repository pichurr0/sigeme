from django.contrib.auth.models import User
from rest_framework import serializers
from .nomenclators import TipoMedio
from .models import Medio, Componente, Equipo, Periferico, Computadora, Ubicacion

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

    id = serializers.IntegerField()
    tipo = serializers.CharField()


class UbicacionSerializer(serializers.ModelSerializer):
    """Serializador de Ubicacion."""

    class Meta:
        model = Ubicacion
        fields = '__all__'


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
    marca = serializers.CharField()
    modelo = serializers.CharField()
    estado = serializers.CharField()
    ubicacion = UbicacionSerializer()

    class Meta:
        # model = Medio
        fields = ['id', 'tipo', 'serie', 'marca', 'modelo', 'estado', 'ubicacion']
        # read_only_fields = ['creacion', 'modificacion']
        # depth = 1  # revisar denuevo esto para que es


class ComponenteSerializer(MedioSerializer, serializers.ModelSerializer):
    """Componentes que van dentro de una computadora."""

    tipo_componente = serializers.CharField()
    tipo_ram = serializers.CharField()
    tipo_capacidad = serializers.CharField()
    tipo_frecuencia = serializers.CharField()

    class Meta:
        model = Componente
        fields = '__all__'


class EquipoSerializer(MedioSerializer,serializers.ModelSerializer):
    """Componentes que van dentro de una computadora."""

    inventario = serializers.CharField()

    class Meta:
        model = Equipo
        fields = '__all__'


class PerifericoSerializer(MedioSerializer,serializers.ModelSerializer):
    """Componentes que van dentro de una computadora."""

    conectado_a = serializers.CharField()
    tipo_periferico = serializers.CharField()

    class Meta:
        model = Periferico
        fields = '__all__'


class ComputadoraSerializer(MedioSerializer,serializers.ModelSerializer):
    """Componentes que van dentro de una computadora."""

    sello = serializers.CharField()

    class Meta:
        model = Computadora
        fields = '__all__'