from django.contrib import admin
from .models import PersonalCDI, Paciente, ControlEndocrino, RutaMaterna, PlanificacionFamiliar, InventarioEquipo

# Registramos los módulos base de forma sencilla primero
admin.site.register(PersonalCDI)
admin.site.register(Paciente)
admin.site.register(ControlEndocrino)
admin.site.register(RutaMaterna)
admin.site.register(PlanificacionFamiliar)
admin.site.register(InventarioEquipo)

# Personalizamos el título del Panel
admin.site.site_header = "Administración del CDI"
admin.site.site_title = "CDI Portal"
admin.site.index_title = "Bienvenido al Sistema Integral del CDI"