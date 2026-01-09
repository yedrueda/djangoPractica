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

    # ... (tu modelo Paciente está arriba) ...

class Consulta(models.Model):
    # Relación: Si borras al paciente, se borran sus consultas (CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='consultas')
    
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Atención")
    motivo = models.CharField(max_length=200, verbose_name="Motivo de Consulta")
    sintomas = models.TextField(verbose_name="Sintomatología")
    diagnostico = models.TextField(verbose_name="Diagnóstico Médico")
    tratamiento = models.TextField(verbose_name="Tratamiento Indicado")
    
    # Datos opcionales (signos vitales)
    presion_arterial = models.CharField(max_length=20, blank=True, null=True)
    temperatura = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    
    def __str__(self):
        return f"Consulta {self.paciente.nombres} - {self.fecha.strftime('%d/%m/%Y')}"

    class Meta:
        ordering = ['-fecha'] # Las más recientes primero
    

from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission

@receiver(post_migrate)
def crear_grupos_permisos(sender, **kwargs):
    if sender.name == 'gestion':
        # 1. Crear Grupos
        admin_group, _ = Group.objects.get_or_create(name='Administrador')
        medico_group, _ = Group.objects.get_or_create(name='Médico')
        recepcion_group, _ = Group.objects.get_or_create(name='Recepción')

        # Aquí podríamos asignar permisos específicos a cada grupo en el futuro
        print("Grupos de seguridad configurados correctamente")