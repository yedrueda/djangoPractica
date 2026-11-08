from django.contrib import admin
from .models import (
    PersonalCDI, Paciente, Turno, ControlEndocrino, ControlRespiratorio, RutaMaterna, 
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

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('tipo_cedula', 'cedula', 'nombre', 'apellido', 'sexo', 'edad', 'grupo_sanguineo', 'comuna', 'sector_cpt', 'prioridad_sugerida_triaje')
    list_filter = ('sexo', 'grupo_sanguineo', 'gestante', 'posee_discapacidad', 'carnet_de_la_patria', 'comuna')
    search_fields = ('cedula', 'nombre', 'apellido', 'telefono', 'direccion', 'alergias', 'antecedentes_personales')
    readonly_fields = ('fecha_registro',)
admin.site.register(Turno)
@admin.register(ControlEndocrino)
class ControlEndocrinoAdmin(admin.ModelAdmin):
    list_display = ('fecha_atencion', 'paciente', 'pas', 'tipo_diabetes', 'glucemia_ayunas', 'hba1c', 'imc', 'riesgo_cardiovascular', 'insulina')
    list_filter = ('pas', 'tipo_diabetes', 'riesgo_cardiovascular', 'diabetes_mellitus', 'hipertension_arterial', 'insulina', 'pie_diabetico', 'obesidad')
    search_fields = ('paciente__cedula', 'paciente__nombre', 'paciente__apellido', 'diagnostico', 'medicamentos_entregados')
    date_hierarchy = 'fecha_atencion'
@admin.register(ControlRespiratorio)
class ControlRespiratorioAdmin(admin.ModelAdmin):
    list_display = ('fecha_atencion', 'paciente', 'pas', 'severidad_cuadro', 'saturacion_oxigeno', 'nebulizacion_realizada', 'resultado_bk')
    list_filter = ('pas', 'severidad_cuadro', 'asma_bronquial', 'epoc', 'infeccion_respiratoria_aguda', 'sospecha_tuberculosis', 'nebulizacion_realizada')
    search_fields = ('paciente__cedula', 'paciente__nombre', 'paciente__apellido', 'diagnostico')
    date_hierarchy = 'fecha_atencion'

@admin.register(RutaMaterna)
class RutaMaternaAdmin(admin.ModelAdmin):
    list_display = ('fecha_control', 'paciente', 'semanas_embarazo', 'formula_obstetrica', 'riesgo_obstetrico', 'frecuencia_cardiaca_fetal', 'eje')
    list_filter = ('pas', 'riesgo_obstetrico', 'vdrl_estatus', 'vih_estatus', 'toxoide_tetanico')
    search_fields = ('paciente__cedula', 'paciente__nombre', 'paciente__apellido', 'eje', 'diagnostico')
    date_hierarchy = 'fecha_control'

@admin.register(PlanificacionFamiliar)
class PlanificacionFamiliarAdmin(admin.ModelAdmin):
    list_display = ('fecha_atencion', 'paciente', 'primera_sucesiva', 'tipo_metodo', 'preservativo_masculino', 'diu', 'implante', 'citologia_realizada')
    list_filter = ('primera_sucesiva', 'tipo_metodo', 'diu', 'implante', 'citologia_realizada')
    search_fields = ('paciente__cedula', 'paciente__nombre', 'paciente__apellido', 'metodo_entregado', 'diagnostico')
    date_hierarchy = 'fecha_atencion'
admin.site.register(InventarioEquipo)

# Personalizamos el título del Panel
admin.site.site_header = "Administración del CDI"
admin.site.site_title = "CDI Portal"
admin.site.index_title = "Bienvenido al Sistema Integral del CDI"