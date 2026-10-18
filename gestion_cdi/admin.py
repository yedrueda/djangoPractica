from django.contrib import admin
from .models import (
    PersonalCDI, Paciente, ControlEndocrino, RutaMaterna, 
    PlanificacionFamiliar, InventarioEquipo, TurnoGuardia,
    Comuna, SectorCPT, IndicadorPoblacionalASIC
)

@admin.register(PersonalCDI)
class PersonalCDIAdmin(admin.ModelAdmin):
    list_display = ('tipo_cedula', 'cedula', 'nombre', 'apellido', 'rol_profesional', 'estatus', 'carnet_de_la_patria')
    list_filter = ('estatus', 'rol_profesional', 'carnet_de_la_patria')
    search_fields = ('cedula', 'nombre', 'apellido')

@admin.register(TurnoGuardia)
class TurnoGuardiaAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'personal', 'tipo_turno', 'area_servicio', 'estado', 'suplente')
    list_filter = ('fecha', 'tipo_turno', 'area_servicio', 'estado')
    search_fields = ('personal__nombre', 'personal__apellido', 'personal__cedula', 'observaciones')
    date_hierarchy = 'fecha'

@admin.register(Comuna)
class ComunaAdmin(admin.ModelAdmin):
    list_display = ('orden', 'nombre', 'total_poblacion', 'total_familias')
    ordering = ('orden',)

@admin.register(SectorCPT)
class SectorCPTAdmin(admin.ModelAdmin):
    list_display = ('numero', 'nombre', 'comuna', 'poblacion', 'familias', 'situacion_espacio', 'medico_responsable')
    list_filter = ('comuna', 'situacion_espacio')
    search_fields = ('nombre', 'medico_responsable', 'observaciones')
    ordering = ('numero',)

@admin.register(IndicadorPoblacionalASIC)
class IndicadorPoblacionalASICAdmin(admin.ModelAdmin):
    list_display = ('poblacion_total', 'familias_total', 'comunas_total', 'femenino_total', 'masculino_total', 'fecha_actualizacion')

admin.site.register(Paciente)
admin.site.register(ControlEndocrino)
admin.site.register(RutaMaterna)
admin.site.register(PlanificacionFamiliar)
admin.site.register(InventarioEquipo)

# Personalizamos el título del Panel
admin.site.site_header = "Administración del CDI"
admin.site.site_title = "CDI Portal"
admin.site.index_title = "Bienvenido al Sistema Integral del CDI"