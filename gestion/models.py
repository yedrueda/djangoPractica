from django.db import models

class Paciente(models.Model):
    # Identificación
    cedula = models.CharField(max_length=15, unique=True, verbose_name="Cédula de Identidad")
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    
    # Datos Demográficos
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")
    direccion = models.TextField(blank=True, null=True, verbose_name="Dirección de Habitación")
    
    # Datos del Sistema
    fecha_registro = models.DateTimeField(auto_now_add=True) # Se llena solo al crear
    
    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.cedula})"
        
    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        ordering = ['apellidos'] # Ordenar alfabéticamente por defecto