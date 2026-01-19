from django.contrib import admin
from .models import Paciente, Consulta

# Esta clase configura cómo se ve el panel de administración
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('cedula', 'nombres', 'apellidos', 'telefono') # Columnas visibles
    search_fields = ('cedula', 'apellidos') # Barra de búsqueda
    #list_filter = ('fecha_registro',) # Filtros a la derecha

# Registramos el modelo
admin.site.register(Paciente, PacienteAdmin)

class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'paciente', 'motivo', 'diagnostico')
    list_filter = ('fecha',)
    search_fields = ('paciente__cedula', 'paciente__apellidos') # Buscamos por datos del paciente relacionado

admin.site.register(Consulta, ConsultaAdmin)