from django.contrib import admin
from .models import Paciente

# Esta clase configura cómo se ve el panel de administración
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('cedula', 'nombres', 'apellidos', 'telefono') # Columnas visibles
    search_fields = ('cedula', 'apellidos') # Barra de búsqueda
    list_filter = ('fecha_registro',) # Filtros a la derecha

# Registramos el modelo
admin.site.register(Paciente, PacienteAdmin)
