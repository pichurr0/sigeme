from django import forms
from django.contrib import admin
from .nomenclators import TipoMarca, TipoModelo, \
    TipoDivision, TipoMunicipio, TipoUnidad, TipoDepartamento, \
    TipoPiso, TipoSistemaOperativo, TipoProvincia, TipoPeriferico, TipoPrograma


# Modelos que van a ser gestionados por el sistema.

class TipoPerifericoAdmin(admin.ModelAdmin):
    """
    no pueden especificarse los 2. O fieldset o fields
    """

    readonly_fields = ["slug"]
    fieldsets = [
        (None, {"fields": ["tipo"]}),
        ("informacion para la web", {"fields": ["slug"]}),
    ]


@admin.register(TipoDivision)
class TipoDivisionAdmin(admin.ModelAdmin):
    list_display = ("tipo", "provincia", "unidades_subordinadas")

    def unidades_subordinadas(self, obj):
        from django.db.models import Count
        from django.utils.html import format_html
        result = TipoUnidad.objects.filter(division=obj).aggregate(Count("id"))
        return format_html("<b><i>{}</i></b>", result["id__count"])

    unidades_subordinadas.short_description = "Unidades Subordinadas (Cant.)"


@admin.register(TipoDepartamento)
class TipoDepartamentoAdmin(admin.ModelAdmin):
    list_display = ("tipo", "division")
    search_fields = ("tipo__startswith", )
    list_filter = ("division__tipo",)


class TipoSistemaOperativoAdminForm(forms.ModelForm):
    class Meta:
        model = TipoSistemaOperativo
        fields = "__all__"

    def clean_tipo(self):
        if self.cleaned_data["tipo"].lower() == "linux":
            raise forms.ValidationError("Espeficique la distribucion de linux")

        return self.cleaned_data["tipo"]


@admin.register(TipoSistemaOperativo)
class TipoSistemaOperativoAdmin(admin.ModelAdmin):
    """

    configurar la vizualizacion de campos en el formulario y sus validaciones.


    """

    fields = ('version', 'tipo')

    # validaciones de formulario
    form = TipoSistemaOperativoAdminForm

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["tipo"].label = "Nombre del SO:"
        return form


admin.site.register(TipoPeriferico, TipoPerifericoAdmin)
admin.site.register(TipoMarca)
admin.site.register(TipoModelo)
admin.site.register(TipoProvincia)
admin.site.register(TipoMunicipio)
admin.site.register(TipoUnidad)
admin.site.register(TipoPiso)
admin.site.register(TipoPrograma)
