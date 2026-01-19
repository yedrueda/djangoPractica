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
    # Opciones de programas
    PROGRAMAS = [
        ('GENERAL', 'Consulta General'),
        ('RESPIRATORIO', 'Programa Respiratorio'),
        ('ENDOCRINO', 'Endocrinometabólico (Diabetes/HTA)'),
        ('RUTA_MATERNA', 'Ruta Materna'),
        ('SSR', 'Salud Sexual y Reproductiva (SSR)'),
    ]

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='consultas')
    fecha = models.DateTimeField(auto_now_add=True)
    
    # Nuevo campo de Programa
    programa = models.CharField(max_length=20, choices=PROGRAMAS, default='GENERAL')
    
    motivo = models.TextField()
    diagnostico = models.TextField()
    tratamiento = models.TextField()
    medico = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.paciente.nombres} - {self.get_programa_display()} ({self.fecha.date()})"


    

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