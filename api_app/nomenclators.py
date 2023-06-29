from django.db import models
from django.utils.translation import gettext_lazy as _


class TipoMedio(models.TextChoices):
    """TipoMedio."""
    EQUIPO = "equipo", _("Equipo")
    PERIFERICO = "periferico", _("Periferico")
    COMPUTADORA = "computadora", _("Computadora")
    COMPONENTE = "componente", _("Componente")


class TipoMarca(models.Model):
    """TipoMarca."""

    tipo = models.CharField(max_length=200)

    class Meta:
        verbose_name = "marca"
        verbose_name_plural = "marcas"

    def __str__(self):
        return self.tipo


class TipoModelo(models.Model):
    """TipoModelo."""

    tipo = models.CharField(max_length=200)
    marca = models.OneToOneField("TipoMarca", on_delete=models.CASCADE)

    def __str__(self):
        return self.tipo

    class Meta:
        verbose_name = "modelo"
        verbose_name_plural = "modelos"


class TipoProvincia(models.Model):
    """TipoProvincia."""

    tipo = models.CharField(max_length=100)

    def __str__(self):
        return self.tipo

    class Meta:
        verbose_name = "provincia"
        verbose_name_plural = "provincias"


class TipoDivision(models.Model):
    """TipoDivision."""

    tipo = models.CharField(max_length=200)
    provincia = models.OneToOneField("TipoProvincia", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "division"
        verbose_name_plural = "divisiones"

    def __str__(self):
        return self.tipo


class TipoMunicipio(models.Model):
    """TipoMunicipio."""

    tipo = models.CharField(max_length=200)
    provincia = models.OneToOneField("TipoProvincia", on_delete=models.CASCADE)

    def __str__(self):
        return self.tipo

    class Meta:
        verbose_name = "municipo"
        verbose_name_plural = "municipos"


class TipoUnidad(models.Model):
    """TipoUnidad."""

    tipo = models.CharField(max_length=200)
    division = models.OneToOneField("TipoDivision", on_delete=models.CASCADE)
    municipio = models.OneToOneField("TipoMunicipio", on_delete=models.CASCADE)

    def __str__(self):
        return self.tipo

    class Meta:
        verbose_name = "unidad"
        verbose_name_plural = "unidades"


class TipoDepartamento(models.Model):
    """revisar con daydee si esto realmente es asi,  parar dpto y piso."""

    tipo = models.CharField(max_length=200)
    division = models.OneToOneField("TipoDivision", on_delete=models.CASCADE)

    def __str__(self):
        return '%d, DIV: %s' % (self.tipo, self.division)

    class Meta:
        verbose_name = "departamento"
        verbose_name_plural = "departamentos"


class TipoPiso(models.Model):
    """TipoPiso."""

    tipo = models.CharField(max_length=200)
    division = models.OneToOneField("TipoUnidad", on_delete=models.CASCADE)

    def __str__(self):
        return self.tipo

    class Meta:
        verbose_name = "no. piso"
        verbose_name_plural = "no. de pisos"


class TipoEstadoMedio(models.Model):
    """Para este modelo se puede usar un discionario de palabras inmutables."""

    tipo = models.CharField(max_length=200)

    def __str__(self):
        return self.tipo

    class Meta:
        verbose_name = "estado del medio"
        verbose_name_plural = "estados de los medios"


class TipoEstadoSello(models.Model):
    """Para este modelo se puede usar un discionario de palabras inmutables."""

    tipo = models.CharField(max_length=200)

    def __str__(self):
        return self.tipo

    class Meta:
        verbose_name = "estado del sello"
        verbose_name_plural = "estado de los sellos"


class TipoComponente(models.Model):
    """
    Los componentes que se pueden encontrar dentro de un medio de tipo PC.

    ej: disco duro, ram, fuente.
    """

    tipo = models.CharField(max_length=200)

    def __str__(self):
        return self.tipo

    class Meta:
        verbose_name = "componente"
        verbose_name_plural = "componentes"


class TipoPeriferico(models.Model):
    """
    Los componentes que se pueden encontrar dentro de un medio de tipo PC.

    ej: disco duro, ram, fuente.
    """

    tipo = models.CharField(max_length=200)
    slug = models.CharField(max_length=50,null=True)

    def __str__(self):
        return self.tipo

    class Meta:
        verbose_name = "tipo de periferico"
        verbose_name_plural = "tipos de perifericos"


class TipoRam(models.Model):
    """TipoRam."""

    tipo = models.CharField(max_length=200)

    def __str__(self):
        return self.tipo

    class Meta:
        verbose_name = "tipo de memoria ram"
        verbose_name_plural = "tipos de memoria ram"


class TipoPrograma(models.Model):
    """Programa."""

    tipo = models.CharField(max_length=200)

    def __str__(self):
        return self.tipo
 
    class Meta:
        verbose_name = "programa"
        verbose_name_plural = "programas"

class TipoSistemaOperativo(models.Model):
    """Sistemas Operativos."""

    tipo = models.CharField(max_length=200)

    def __str__(self):
        return self.tipo

    class Meta:
        verbose_name = "sistema operativo"
        verbose_name_plural = "sistemas operativos"
