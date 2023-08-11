import random
from django import forms
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html
from django.contrib import admin
from .nomenclators import TipoMarca, TipoModelo, \
    TipoDivision, TipoMunicipio, TipoUnidad, TipoDepartamento, \
    TipoPiso, TipoSistemaOperativo, TipoProvincia, TipoPeriferico, TipoPrograma


class TipoPerifericoAdmin(admin.ModelAdmin):
    """
    no pueden especificarse los 2. O fieldset o fields
    """

    readonly_fields = ["slug"]
    fieldsets = [
        (None, {"fields": ["tipo"]}),
        ("informacion para la web", {"fields": ["slug"]}),
    ]

admin.site.register(TipoPeriferico, TipoPerifericoAdmin)


@admin.register(TipoDivision)
class TipoDivisionAdmin(admin.ModelAdmin):
    """
    Adicionar informacion sobre las unidades con las que cuenta la division
    """
    
    list_display = ("tipo", "provincia", "unidades_subordinadas")
    list_display_links = ('tipo',)

    def unidades_subordinadas(self, obj):
        from django.db.models import Count
        result = TipoUnidad.objects.filter(division=obj).aggregate(Count("id"))
        return format_html("<b><i>{}</i></b>", result["id__count"])

    unidades_subordinadas.short_description = "Unidades Subordinadas (Cant.)"


@admin.register(TipoDepartamento)
class TipoDepartamentoAdmin(admin.ModelAdmin):
    """
	filtrado y ordeniento de los elementos listados para mejor ux
	"""
    list_display = ("tipo", "division")
    search_fields = ("tipo__startswith", )
    list_filter = ("division__tipo",)


class TipoSistemaOperativoAdminForm(forms.ModelForm):
    """
    Modifica el comportamiento del formulario para Tipos de Sistema Operativo
    """

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
    form = TipoSistemaOperativoAdminForm

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["tipo"].label = "Nombre del SO:"
        return form


@admin.register(TipoUnidad)
class TipoUnidadAdmin(admin.ModelAdmin):
    """
    Configurar enlace para que el ultimo elemento de la tabla redireccione a division

    """

    list_display = ('tipo', 'municipio', 'division', 'view_division_link')
    empty_value_display = "--seleccione--"

    def view_division_link(self, obj):
        count = random.randint(1, 10)
        url = (
            reverse("admin:api_app_tipodivision_changelist")
            + "?"
            # + urlencode({"tipounidad__id": f"{obj.id}"})
            + urlencode({"id": f"{obj.division.id}"})
        )
        return format_html('<a href="{}">Apunta a ID Division {} </a>', url, obj.division.id)

    view_division_link.short_description = "Link Division"

admin.site.register(TipoMarca)
admin.site.register(TipoModelo)
admin.site.register(TipoProvincia)
admin.site.register(TipoMunicipio)
admin.site.register(TipoPiso)
admin.site.register(TipoPrograma)
