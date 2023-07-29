from datetime import datetime
from django.db import models
from django.utils import timezone
from api_app.nomenclators import *

# "CONCRETE TABLE INHERITANCE" en modelo Medio, [No se puede implementar con
# rest_framework porque no existe un AbstractClassSerializer]


class Persona(models.Model):
    """Representa un responsable de un medio."""

    nombre = models.CharField(max_length=200)
    ubicacion = models.ForeignKey("Ubicacion", on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "api_persona"


class Ubicacion(models.Model):
    """
    Representa la ubicion de un medio.

    donde se encuentra fisicamente localizado.
    """

    division = models.OneToOneField("TipoDivision",  on_delete=models.RESTRICT)
    municipio = models.OneToOneField("TipoMunicipio", on_delete=models.RESTRICT)  # noqa: E501
    unidad = models.OneToOneField("TipoUnidad", on_delete=models.DO_NOTHING)
    departamento = models.OneToOneField("TipoDepartamento",
               on_delete=models.DO_NOTHING)  # noqa: E128
    piso = models.OneToOneField("TipoPiso", null=True, on_delete=models.DO_NOTHING)  # noqa: E501
    text = models.CharField(max_length=500, null=True)

    class Meta:
        db_table = "api_ubicacion"
    
    def __str__(self):
         return f'{self.division.tipo}, {self.municipio.tipo}, {self.departamento.tipo}, {self.unidad.tipo}, {self.piso.tipo}'


class Medio(models.Model):
    """
    Representa la clase abstranta "Medio Basico".

    con los atributos generales a las clases hijas.
    """

    # require pillow    foto = models.ImageField(blank=True,null=True)
    tipo = models.CharField(max_length=21, null=False, blank=False,
            choices=TipoMedio.choices,  # noqa: E128
            default=TipoMedio.EQUIPO,)  # noqa: E128, E501
    serie = models.CharField(max_length=200, blank=True)
    marca = models.ForeignKey("TipoMarca",
            default=TipoMarca.objects.get(id=1).id,  # noqa: E128
            on_delete=models.CASCADE)  # noqa: E128
    modelo = models.ForeignKey("TipoModelo", null=True,
            default=TipoModelo.objects.get(id=1).id,  # noqa: E128
            on_delete=models.RESTRICT)  # noqa: E128
    estado = models.CharField(max_length=21, null=False, blank=False,
            choices=TipoEstadoMedio.choices,  # noqa: E128
            default=TipoEstadoMedio.BIEN,)  # noqa: E128, E501
    ubicacion = models.ForeignKey("Ubicacion", null=True, on_delete=models.CASCADE)  # noqa: E501
    responsable = models.ForeignKey("Persona", null=True, on_delete=models.CASCADE)  # noqa: E501

    creacion = models.DateTimeField(default=timezone.now)
    modificacion = models.DateTimeField(default=timezone.now)

    class Meta:
        # ordering = ['-id']  # ORDER BY not allowed in subqueries of compound statements.
        db_table = "api_medio"
        indexes = [
            models.Index(fields=['tipo']),
        ]

    def __str__(self):
        return f'{self.tipo} : {self.id}'

    def extraer_movimiento(self):
        raise NotImplementedError


class Equipo(Medio):
    """Medios que no son Perifericos o Coputadoras."""

    inventario = models.CharField(max_length=200, blank=False)

    class Meta:
        db_table = "api_equipo"

    def extraer_movimiento(self):
        return Movimiento(
            medio=self,
            tipo=self.tipo,
            estado=self.estado,
            serie=self.serie,
            responsable=self.responsable.__str__(),
            ubicacion=self.ubicacion.__str__(),
            sello_inv=self.inventario
            )


class Periferico(Medio):
    """Perifericos."""

    conectado_a = models.ForeignKey("Medio",
        blank=True,  # noqa: E128
        null=True,  # noqa: E128
        on_delete=models.SET_NULL,  # noqa: E128
        verbose_name="conexion",  # noqa: E128
        related_name="tags",  # noqa: E128
        related_query_name="tag",)  # noqa: E128
    tipo_periferico = models.ForeignKey("TipoPeriferico", on_delete=models.RESTRICT)

    class Meta:
        db_table = "api_periferico"

    def extraer_movimiento(self):
        return Movimiento(
            medio=self,
            tipo=self.tipo,
            estado=self.estado,
            serie=self.serie,
            responsable=self.responsable.__str__(),
            ubicacion=self.ubicacion.__str__(),
            sello_inv=''
            )


class Computadora(Medio):
    """Computadora."""

    ip = models.GenericIPAddressField()
    sistema_operativo = models.ForeignKey("TipoSistemaOperativo", on_delete=models.RESTRICT)  # noqa: E501
    mac = models.CharField(max_length=200)
    usuario = models.CharField(max_length=200, blank=True, null=True)
    nombrepc = models.CharField(max_length=200, blank=True, null=True)
    sello = models.CharField(max_length=200, blank=True, null=True)
    estado_sello = models.CharField(max_length=21, null=False, blank=False,
            choices=TipoEstadoSello.choices,  # noqa: E128
            default=TipoEstadoSello.BIEN,)  # noqa: E128, E501
    es_servidor = models.BooleanField(default=False)
    servicio = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = "api_computadora"

    @property
    def componentes(self):
        return Componente.objects.filter(medio=self.id).count()

    def extraer_movimiento(self):
        return Movimiento(
            medio=self,
            tipo=self.tipo,
            estado=self.estado,
            serie=self.serie,
            responsable=self.responsable.__str__(),
            ubicacion=self.ubicacion.__str__(),
            sello_inv=self.sello
            )


class Componente(Medio):
    """Componentes dentro de la Computadora."""

    medio = models.ForeignKey("Computadora", blank=False, null=True, on_delete=models.RESTRICT)  # noqa: E501
    tipo_componente = models.CharField(max_length=21, null=False, blank=False,
            choices=TipoComponente.choices,  # noqa: E128
            default=TipoComponente.DISCO,)
    tipo_ram = models.CharField(max_length=200, null=True, choices=TipoRam.choices)
    capacidad = models.CharField(max_length=200, null=True)
    frecuencia = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = "api_componente"


class MovimientoComponente(models.Model):
    """
    Refleja las computadoras por las que puede haber pasado un componente .
    """

    componente = models.ForeignKey("Componente", on_delete=models.DO_NOTHING)  # noqa: E501
    serie = models.CharField(max_length=200,)  # serial de la computadora
    sello = models.CharField(max_length=200,)  # sello de la computadora
    computadora = models.ForeignKey("Computadora", on_delete=models.DO_NOTHING)
    fecha = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "api_movimiento_componente"

# fixme, mequede implementando los movimientos de los medios
#  hacer metodo en los medios que devueltan los datos para rellenar el movimiento
class Movimiento(models.Model):
    """
    Refleja los cambios de ubicacion de los medios,
    ademas de modifiicacionens en los datos en el medio.
    """

    medio = models.ForeignKey("Medio", blank=False, null=True, on_delete=models.RESTRICT)  # noqa: E501
    tipo = models.CharField(max_length=200,)
    estado = models.CharField(max_length=200,)
    serie = models.CharField(max_length=200,)
    responsable = models.CharField(max_length=200,)
    ubicacion = models.CharField(max_length=200,)
    sello_inv = models.CharField(max_length=200,)
    fecha = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "api_movimiento"
