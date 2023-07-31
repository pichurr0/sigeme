from sigeme_project import logger
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .nomenclators import TipoMedio, TipoMarca, TipoModelo, TipoSistemaOperativo, TipoPeriferico
from .models import Medio, Componente, Equipo, Periferico, Computadora, \
    Ubicacion, MovimientoComponente, Movimiento


class UserSerializer(serializers.ModelSerializer):
    """Serializaror de Usuarios. 
     antes serializers.HyperlinkedModelSerializer de tal
     forma que se ponian los atributos url y is_staff

       Este modelo en la api tendra un atributo url en el que se podran ver todos los detalles del mismo
    """

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
                email=validated_data['email'],
                username=validated_data['username']
                )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user


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
        logger.info('tremendo')
        print('marca serializer')


class ModeloSerializer(NomencladorSerializer, serializers.ModelSerializer):
    """Serializador para datos que no tienen una representacion en forma de modelo."""
    
    marca = serializers.PrimaryKeyRelatedField(queryset=TipoMarca.objects.all())

    class Meta:
        model = TipoModelo
        fields = ['id', 'tipo', 'marca']

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

    tipo = serializers.StringRelatedField()

    class Meta:
        model = TipoMedio
        exclude = ['slug']


class MedioSerializer(serializers.Serializer):
    """Serializador de Medio. [Serializador padre para todas los hijos de medio basico]
       antiguamente defifnida asi MedioSerializer(serializers.ModelSerializer):
    Ni convirtiendo esta clase a Serializer se pueden solicitar atributos
    de las clases hijas. Dichos attrs no se encuentran en la clase medio.
    """
    id = serializers.IntegerField(label='ID', read_only=True)
    # foto = serializers.ImageField(blank=True,null=True)
    tipo = serializers.CharField()
    serie = serializers.CharField()
    # marca = serializers.CharField()
    # marca = NomencladorSerializer()
    marca = serializers.PrimaryKeyRelatedField(queryset=TipoMarca.objects.all())
    modelo = ModeloSerializer()
    estado = serializers.CharField()
    ubicacion = serializers.PrimaryKeyRelatedField(queryset=Ubicacion.objects.all())
    creacion = serializers.DateTimeField(
        default=serializers.CreateOnlyDefault(timezone.now)
    )
    modificacion = serializers.DateTimeField(
        read_only=True, required=False,
        default=timezone.now
    )

    class Meta:
        model = Medio
        fields = ['id', 'tipo', 'serie', ]  # 'marca', 'modelo', 'estado', 'ubicacion'
        read_only_fields = ['creacion', 'modificacion']
        depth = 1  # revisar denuevo esto para que es


class ComponenteSerializer(MedioSerializer, serializers.ModelSerializer):
    """Componentes que van dentro de una computadora."""

    medio = serializers.PrimaryKeyRelatedField(queryset=Computadora.objects.all())
    tipo_componente = serializers.CharField()
    tipo_ram = serializers.CharField(required=False, allow_null=True)
    capacidad = serializers.CharField(required=False, allow_null=True)
    frecuencia = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = Componente
        fields = '__all__'

    def create(self, validated_data):
        """
        Fue necesario sobrescribir este metodo
        """

        data = validated_data

        modelo = TipoModelo.objects.filter(id=validated_data['modelo']['id']).first()
        if modelo:
            data['modelo'] = modelo

        return Componente.objects.create(**data)
    
    def update(self, instance, validated_data):
        """AssertionError: The `.update()` method does not support writable
        nested fields by default. Write an explicit `.update()` method for
        serializer `api_app.serializer.EquipoSerializer`, or set
        `read_only=True` on nested serializer fields

        """

        data = validated_data
        make_move = False
        if data.get('medio') and instance.medio.id != data.get('medio').id:
            make_move = True
            movimiento = MovimientoComponente.objects.create(
                componente=instance,
                serie=instance.medio.serie,
                sello=instance.medio.sello,
                computadora=instance.medio,
                )

        instance.medio = data.get('medio')
        instance.capacidad = data.get('capacidad')
        instance.frecuencia = data.get('frecuencia')
        instance.tipo_ram = data.get('tipo_ram')

        # revision de modelo porque es un writable nested field
        modelo = TipoModelo.objects.get(id=data['modelo']['id'])
        if modelo:
            data['modelo'] = modelo
        instance.modelo = modelo
        # Persistir los datos validados en el objecto instancia
        instance.save()

        if make_move:
            movimiento.save()
        return instance


class EquipoSerializer(MedioSerializer, serializers.ModelSerializer):
    """Componentes que van dentro de una computadora."""

    inventario = serializers.CharField()

    class Meta:
        model = Equipo
        fields = '__all__'

    def create(self, validated_data):
        """
        Fue necesario sobrescribir este metodo
        """

        print('en el serializer.py create')
        logger.info(f'dentro de serialize {validated_data}')

        data = validated_data

        modelo = TipoModelo.objects.filter(id=validated_data['modelo']['id']).first()
        if modelo:
            data['modelo'] = modelo

        return Equipo.objects.create(**data)

    def update(self, instance, validated_data):
        """AssertionError: The `.update()` method does not support writable
        nested fields by default. Write an explicit `.update()` method for
        serializer `api_app.serializer.EquipoSerializer`, or set
        `read_only=True` on nested serializer fields

        Aqui todavia no se guarda en base de datos
        """
        print('en el serializer.py update')

        data = validated_data
        instance.inventario = data['inventario']
        instance.serie = data['serie']

        movimiento = instance.extraer_movimiento()
        # revision de modelo porque es un writable nested field
        modelo = TipoModelo.objects.get(id=data['modelo']['id'])
        if modelo:
            data['modelo'] = modelo
        instance.modelo = modelo
        # Persistir los datos validados en el objecto instancia
        instance.save()
        movimiento.save()
        return instance


class PerifericoSerializer(MedioSerializer, serializers.ModelSerializer):
    """Equipos que son perifericos a la computadora."""

    conectado_a = serializers.PrimaryKeyRelatedField(queryset=Medio.objects.all(), required=False, allow_null=True)  # noqa: E501
    tipo_periferico = serializers.PrimaryKeyRelatedField(queryset=TipoPeriferico.objects.all())

    class Meta:
        model = Periferico
        fields = '__all__'

    def create(self, validated_data):
        """
        Fue necesario sobrescribir este metodo
        """

        data = validated_data

        modelo = TipoModelo.objects.filter(id=validated_data['modelo']['id']).first()
        if modelo:
            data['modelo'] = modelo

        return Periferico.objects.create(**data)
    
    def update(self, instance, validated_data):
        """AssertionError: The `.update()` method does not support writable
        nested fields by default. Write an explicit `.update()` method for
        serializer `api_app.serializer.EquipoSerializer`, or set
        `read_only=True` on nested serializer fields

        """

        data = validated_data
        movimiento = instance.extraer_movimiento()
        instance.conectado_a = data['conectado_a']
        instance.tipo_periferico = data['tipo_periferico']
        instance.serie = data['serie']

        # revision de modelo porque es un writable nested field
        modelo = TipoModelo.objects.get(id=data['modelo']['id'])
        if modelo:
            data['modelo'] = modelo
        instance.modelo = modelo
        # Persistir los datos validados en el objecto instancia
        instance.save()
        movimiento.save()
        return instance


class ComputadoraSerializer(MedioSerializer, serializers.ModelSerializer):
    """Componentes que van dentro de una computadora."""

    sello = serializers.CharField()
    estado_sello = serializers.CharField()
    mac = serializers.CharField()
    ip = serializers.CharField()
    usuario = serializers.CharField()
    sistema_operativo = serializers.PrimaryKeyRelatedField(queryset=TipoSistemaOperativo.objects.all())
    componentes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Computadora
        fields = '__all__'

    def create(self, validated_data):
        """
        Fue necesario sobrescribir este metodo
        """

        data = validated_data

        modelo = TipoModelo.objects.filter(id=validated_data['modelo']['id']).first()
        if modelo:
            data['modelo'] = modelo

        return Computadora.objects.create(**data)
    
    def update(self, instance, validated_data):
        """AssertionError: The `.update()` method does not support writable
        nested fields by default. Write an explicit `.update()` method for
        serializer `api_app.serializer.EquipoSerializer`, or set
        `read_only=True` on nested serializer fields

        Aqui todavia no se guarda en base de datos
        """

        data = validated_data
        movimiento = instance.extraer_movimiento()
        instance.ip = data['ip']
        instance.mac = data['mac']
        instance.nombrepc = data['nombrepc']
        instance.usuario = data['usuario']
        instance.es_servidor = data['es_servidor']
        instance.sistema_operativo = data['sistema_operativo']
        instance.serie = data['serie']

        # revision de modelo porque es un writable nested field
        modelo = TipoModelo.objects.get(id=data['modelo']['id'])
        if modelo:
            data['modelo'] = modelo
        instance.modelo = modelo
        # Persistir los datos validados en el objecto instancia
        instance.save()
        movimiento.save()
        return instance


class MovimientoSerializer(serializers.ModelSerializer):
    """
    Serializador para los movimientos de los medios
    """

    fecha = serializers.DateTimeField(read_only=True)
    medio = serializers.CharField(read_only=True)
    tipo = serializers.CharField(read_only=True)
    estado = serializers.CharField(read_only=True)
    serie = serializers.CharField(read_only=True)
    responsable = serializers.CharField(read_only=True)
    ubicacion = serializers.CharField(read_only=True)
    sello_inv = serializers.CharField(read_only=True)


class MovimientoComponenteSerializer(serializers.ModelSerializer):
    """
    Serializador para los movimientos de los medios
    """

    fecha = serializers.DateTimeField(read_only=True)
    componente = serializers.CharField(read_only=True)
    serie = serializers.CharField(read_only=True)
    computadora = serializers.CharField(read_only=True)

    