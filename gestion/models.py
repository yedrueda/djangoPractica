from django.db import models
from django.contrib.auth.models import User

class Paciente(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20, unique=True)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=20)
    direccion = models.TextField()
    # Agrega esta línea exactamente así:
    fecha_registro = models.DateTimeField(auto_now_add=True, null=True, blank=True) 

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
    
    # Campos específicos (CORREGIDO: Sin placeholder)
    fur = models.DateField(null=True, blank=True, verbose_name="Fecha de Última Regla")
    tension_arterial = models.CharField(max_length=10, null=True, blank=True)
    peso_madre = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    glicemia = models.IntegerField(null=True, blank=True)

    @property
    def semanas_gestacion(self):
        if self.fur:
            from datetime import date
            dias = (date.today() - self.fur).days
            return f"{dias // 7} Semanas"
        return None
    
    def __str__(self):
        return f"{self.paciente.nombres} - {self.get_programa_display()}"