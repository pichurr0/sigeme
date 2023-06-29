from django.contrib import admin
from .nomenclators import TipoMarca, TipoModelo, \
    TipoDivision, TipoMunicipio, TipoUnidad, TipoDepartamento, \
    TipoPiso, TipoEstadoMedio, TipoEstadoSello, TipoComponente, \
    TipoProvincia, TipoPeriferico, TipoRam, TipoPrograma, \
    TipoSistemaOperativo

# Modelos que van a ser gestionados por el sistema.

class TipoPerifericoAdmin(admin.ModelAdmin):
    # no pueden especificarse los 2. O fieldset o fields
    # fields = ["tipo", "slug"]
    fieldsets = [
        (None, {"fields": ["tipo"]}),
        ("informacion para la web", {"fields": ["slug"]}),
    ]


admin.site.register(TipoMarca)
admin.site.register(TipoModelo)
admin.site.register(TipoProvincia)
admin.site.register(TipoDivision)
admin.site.register(TipoMunicipio)
admin.site.register(TipoDepartamento)
admin.site.register(TipoUnidad)
admin.site.register(TipoPiso)
admin.site.register(TipoEstadoMedio)
admin.site.register(TipoEstadoSello)
admin.site.register(TipoComponente)
admin.site.register(TipoPeriferico, TipoPerifericoAdmin)
admin.site.register(TipoRam)
admin.site.register(TipoPrograma)
admin.site.register(TipoSistemaOperativo)