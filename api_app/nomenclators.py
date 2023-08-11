from django.db import models
from django.utils.translation import gettext_lazy as _


class TipoMedio(models.TextChoices):
    """Tipo Medio."""
    EQUIPO = "equipo", _("Equipo")
    PERIFERICO = "periferico", _("Periferico")
    COMPUTADORA = "computadora", _("Computadora")
    COMPONENTE = "componente", _("Componente")


class TipoEstadoMedio(models.TextChoices):
    """Tipo Estado Medio. """
    BIEN = "bien", _("Bien")
    REPARACION = "reparacion", _("Reparacion")
    ROTO = "roto", _("Roto")


class TipoComponente(models.TextChoices):
    """Tipo Componente."""

    RAM = "ram", _("Ram")
    DISCO = "disco", _("Disco Duro")


class TipoRam(models.TextChoices):
    """Tipo Ram.
    tambien se puede escribir asi
    choices=models.TextChoices("Ram", "DDR1 DDR2 DDR3 DDR4").choices
    """

    DDR1 = "ddr1"
    DDR2 = "ddr2"
    DDR3 = "ddr3"
    DDR4 = "ddr4"


class TipoEstadoSello(models.TextChoices):
    """Tipo estado de sello."""

    BIEN = "B"
    SIN_SELLO = "S"
    ROTO = "R"


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
    provincia = models.ForeignKey("TipoProvincia", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "division"
        verbose_name_plural = "divisiones"

    def __str__(self):
        return self.tipo


class TipoMunicipio(models.Model):
    """TipoMunicipio."""

    tipo = models.CharField(max_length=200)
    provincia = models.ForeignKey("TipoProvincia", on_delete=models.CASCADE)

    def __str__(self):
        return self.tipo

    class Meta:
        verbose_name = "municipo"
        verbose_name_plural = "municipos"


class TipoUnidad(models.Model):
    """TipoUnidad."""

    tipo = models.CharField(max_length=200)
    division = models.ForeignKey("TipoDivision", on_delete=models.CASCADE)
    municipio = models.ForeignKey("TipoMunicipio", on_delete=models.CASCADE)

    def __str__(self):
        return self.tipo

    class Meta:
        verbose_name = "unidad"
        verbose_name_plural = "unidades"


class TipoDepartamento(models.Model):
    """revisar con daydee si esto realmente es asi,  parar dpto y piso."""

    tipo = models.CharField(max_length=200)
    division = models.ForeignKey("TipoDivision", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tipo}'

    class Meta:
        verbose_name = "departamento"
        verbose_name_plural = "departamentos"


class TipoPiso(models.Model):
    """TipoPiso."""

    tipo = models.CharField(max_length=200)
    unidad = models.ForeignKey("TipoUnidad", on_delete=models.CASCADE)

    def __str__(self):
        return self.tipo

    class Meta:
        verbose_name = "no. piso"
        verbose_name_plural = "no. de pisos"


class TipoPeriferico(models.Model):
    """
    Los componentes que se pueden encontrar dentro de un medio de tipo PC.

    ej: impresora, teclado, mouse.
    """

    tipo = models.CharField(max_length=200)
    slug = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.tipo

    class Meta:
        verbose_name = "tipo de periferico"
        verbose_name_plural = "tipos de perifericos"


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
    version = models.CharField(max_length=20, default='10')

    def __str__(self):
        return f'{self.tipo} {self.version}'

    class Meta:
        verbose_name = "sistema operativo"
        verbose_name_plural = "sistemas operativos"
