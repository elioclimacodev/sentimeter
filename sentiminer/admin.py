from django.contrib import admin
from .models import ArchivoAnalisis, ResultadoLinea, ResumenAnalisis


@admin.register(ArchivoAnalisis)
class ArchivoAnalisisAdmin(admin.ModelAdmin):
    list_display = ['nombre_original', 'fecha_subida']
    search_fields = ['nombre_original']
    readonly_fields = ['fecha_subida']


class ResultadoLineaInline(admin.TabularInline):
    model = ResultadoLinea
    fields = ['numero_linea', 'texto', 'clasificacion', 'puntaje_polaridad']
    readonly_fields = ['numero_linea', 'texto', 'clasificacion', 'puntaje_polaridad']
    extra = 0
    can_delete = False
    max_num = 0


@admin.register(ResultadoLinea)
class ResultadoLineaAdmin(admin.ModelAdmin):
    list_display = ['archivo', 'numero_linea', 'clasificacion', 'puntaje_polaridad', 'libreria_usada']
    list_filter = ['clasificacion', 'libreria_usada']
    search_fields = ['texto']


@admin.register(ResumenAnalisis)
class ResumenAnalisisAdmin(admin.ModelAdmin):
    list_display = [
        'archivo', 'total_lineas', 'sentimiento_predominante',
        'porcentaje_positivo', 'porcentaje_negativo', 'porcentaje_neutro'
    ]
    readonly_fields = [
        'total_lineas', 'positivas', 'negativas', 'neutras',
        'porcentaje_positivo', 'porcentaje_negativo', 'porcentaje_neutro',
        'sentimiento_predominante'
    ]