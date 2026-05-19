from django.db import models
from django.contrib.auth.models import User

# --- 1. EJE DE PERSONAL ---
class PersonalCDI(models.Model):
    TIPO_DOC = [('V', 'Venezolano'), ('E', 'Extranjero')]
    tipo_cedula = models.CharField(max_length=1, choices=TIPO_DOC, default='V') # <-- NUEVO CAMPO
    cedula = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    ROLES = [('Médico', 'Médico'), ('Enfermero', 'Enfermero'), ('Administrativo', 'Administrativo'), ('Mantenimiento', 'Mantenimiento'), ('Obrero', 'Obrero')]
    rol_profesional = models.CharField(max_length=50, choices=ROLES)
    especialidad = models.CharField(max_length=100, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    ESTATUS = [('Activo', 'Activo'), ('Permiso', 'Permiso'), ('Retirado', 'Retirado')]
    estatus = models.CharField(max_length=20, choices=ESTATUS, default='Activo')
    usuario = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True) # Conexión al login
    fecha_ingreso = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.rol_profesional}: {self.nombre} {self.apellido}"

    class Meta:
        verbose_name_plural = "Personal del CDI"


# --- 2. EJE PACIENTES ---
class Paciente(models.Model):
    TIPO_DOC = [('V', 'Venezolano'), ('E', 'Extranjero')]
    tipo_cedula = models.CharField(max_length=1, choices=TIPO_DOC, default='V') # <-- NUEVO CAMPO
    cedula = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    SEXO = [('M', 'Masculino'), ('F', 'Femenino')]
    sexo = models.CharField(max_length=1, choices=SEXO)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    asic = models.CharField(max_length=100, verbose_name="ASIC")
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cedula} - {self.nombre} {self.apellido}"


# --- 3. PROGRAMAS DE SALUD ---
class ControlEndocrino(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha_atencion = models.DateField(auto_now_add=True)
    tension_arterial = models.CharField(max_length=10, null=True, blank=True)
    peso_kg = models.DecimalField(max_digits=5, decimal_places=2)
    talla_cm = models.IntegerField()
    imc = models.DecimalField(max_digits=4, decimal_places=2)
    hba1c = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name="HbA1c")
    diagnostico = models.TextField(null=True, blank=True)
    tratamiento = models.TextField(null=True, blank=True)
    atendido_por = models.ForeignKey(PersonalCDI, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = "Controles Endocrinos"

class RutaMaterna(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha_control = models.DateField(auto_now_add=True)
    semanas_embarazo = models.IntegerField()
    eje = models.CharField(max_length=100)
    direccion_detallada = models.TextField(null=True, blank=True)
    atendido_por = models.ForeignKey(PersonalCDI, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = "Ruta Materna"

class PlanificacionFamiliar(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha_atencion = models.DateField(auto_now_add=True)
    SUCESIVA = [('Primera', 'Primera'), ('Sucesiva', 'Sucesiva')]
    primera_sucesiva = models.CharField(max_length=20, choices=SUCESIVA)
    metodo_entregado = models.CharField(max_length=100)
    preservativo_masculino = models.IntegerField(default=0)
    atendido_por = models.ForeignKey(PersonalCDI, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = "Planificación Familiar"

class ControlEndocrino(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='controles')
    medico_tratante = models.ForeignKey(PersonalCDI, on_delete=models.SET_NULL, null=True)
    
    fecha_atencion = models.DateField(auto_now_add=True)
    
    # Signos Vitales (Ahora son opcionales con null=True, blank=True)
    tension_arterial = models.CharField(max_length=10, null=True, blank=True, help_text="Ej: 120/80")
    frecuencia_cardiaca = models.IntegerField(null=True, blank=True, help_text="LPM")
    frecuencia_respiratoria = models.IntegerField(null=True, blank=True, help_text="RPM")
    temperatura = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, help_text="°C")
    peso_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Kg")
    talla_cm = models.IntegerField(null=True, blank=True, help_text="cm")
    
    # Exámenes y Diagnóstico
    glucemia_ayunas = models.IntegerField(null=True, blank=True, help_text="mg/dL")
    diagnostico = models.TextField(null=True, blank=True)
    tratamiento = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Consulta: {self.paciente.nombre} {self.paciente.apellido} - {self.fecha_atencion}"


# --- 4. EJE INFRAESTRUCTURA E INVENTARIO ---
class InventarioEquipo(models.Model):
    codigo_bien_nacional = models.CharField(max_length=50, unique=True)
    nombre_equipo = models.CharField(max_length=100)
    TIPO = [('Médico', 'Médico'), ('Electrónico', 'Electrónico'), ('Mobiliario', 'Mobiliario')]
    tipo_equipo = models.CharField(max_length=50, choices=TIPO)
    ubicacion_especifica = models.CharField(max_length=100)
    ESTADO = [('Operativo', 'Operativo'), ('Dañado', 'Dañado'), ('En Reparación', 'En Reparación')]
    estado_fisico = models.CharField(max_length=20, choices=ESTADO, default='Operativo')
    responsable = models.ForeignKey(PersonalCDI, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.codigo_bien_nacional} - {self.nombre_equipo}"
    
    class Meta:
        verbose_name_plural = "Inventario de Equipos"




    
