from django.db import models

from django.db import models
from django.contrib.auth.models import User

class Paciente(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20, unique=True)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=20)
    direccion = models.TextField()

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class Consulta(models.Model):
    PROGRAMAS = [
        ('GENERAL', 'Consulta General'),
        ('RESPIRATORIO', 'Programa Respiratorio'),
        ('ENDOCRINO', 'Endocrinometabólico'),
        ('RUTA_MATERNA', 'Ruta Materna'),
        ('SSR', 'Salud Sexual y Reproductiva'),
    ]
    
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='consultas')
    fecha = models.DateTimeField(auto_now_add=True)
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