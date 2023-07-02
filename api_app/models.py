from datetime import datetime
from django.db import models
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
    text = models.CharField(max_length=500,null=True)

    class Meta:
        db_table = "api_ubicacion"


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
            on_delete=models.CASCADE)  # noqa: E128
    estado = models.ForeignKey("TipoEstadoMedio",
            default=TipoEstadoMedio.objects.get(id=1).id,  # noqa: E128
            on_delete=models.CASCADE)  # noqa: E128
    ubicacion = models.ForeignKey("Ubicacion", null=True, on_delete=models.CASCADE)  # noqa: E501
    responsable = models.ForeignKey("Persona", null=True, on_delete=models.CASCADE)  # noqa: E501

    creacion = models.DateTimeField(default=datetime.now())
    modificacion = models.DateTimeField(default=datetime.now())

    class Meta:
        # ordering = ['-id']  # ORDER BY not allowed in subqueries of compound statements.
        db_table = "api_medio"
        indexes = [
            models.Index(fields=['tipo']),
        ]

    def __str__(self):
        return self.tipo


class Equipo(Medio):
    """Medios que no son Perifericos o Coputadoras."""

    inventario = models.CharField(max_length=200, blank=False)

    class Meta:
        db_table = "api_equipo"


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


class Computadora(Medio):
    """Computadora."""

    ip = models.CharField(max_length=200)
    sistema_operativo = models.ForeignKey("TipoSistemaOperativo", on_delete=models.RESTRICT)  # noqa: E501
    servicio = models.CharField(max_length=200)
    usuario = models.CharField(max_length=200)
    mac = models.CharField(max_length=200)
    nombrepc = models.CharField(max_length=200)
    sello = models.CharField(max_length=200)
    estado_sello = models.ForeignKey("TipoEstadoSello", blank=False, on_delete=models.RESTRICT)  # noqa: E501
    es_servidor = models.BooleanField(default=False)
    componentes = models.ManyToManyField("Componente", related_name="componentes")  # noqa: E501

    class Meta:
        db_table = "api_computadora"

    def get_componentes(self):
        pass


class Componente(Medio):
    """Componentes dentro de la Computadora."""

    tipo_componente = models.ForeignKey("TipoComponente", blank=False, on_delete=models.RESTRICT)
    tipo_ram = models.ForeignKey("TipoRam", null=True, on_delete=models.RESTRICT)
    tipo_capacidad = models.CharField(max_length=200, null=True)
    tipo_frecuencia = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = "api_componente"


