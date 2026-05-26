from django.db import models
from django.contrib.auth.models import User
from datetime import date

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

    @property
    def edad(self):
        if self.fecha_nacimiento:
            hoy = date.today()
            # La fórmula matemática para calcular años exactos
            edad_calculada = hoy.year - self.fecha_nacimiento.year - ((hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))
            return f"{edad_calculada} años"
        return "Sin registro"
    
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
    observaciones = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Ruta Materna"

class PlanificacionFamiliar(models.Model):
    # Relación con el paciente
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha_atencion = models.DateField(auto_now_add=True)
    
    # 1. Control Operativo Regional
    semana = models.IntegerField(null=True, blank=True, verbose_name="Semana Epidemiológica")
    primera_sucesiva = models.CharField(max_length=20, default='Primera')
    establecimiento_salud = models.CharField(max_length=100, default='CDI El Llanito')
    municipio = models.CharField(max_length=100, default='Sucre')
    
    # 2. Métodos de Barrera / Anticonceptivos
    preservativo_masculino = models.IntegerField(default=0)
    metodo_entregado = models.CharField(max_length=100, null=True, blank=True)
    diu = models.CharField(max_length=20, default='No')
    implante = models.CharField(max_length=20, default='No')
    
    # 3. Diagnóstico e Historial
    antecedente_obstetrico = models.TextField(null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"Planificación Familiar - {self.paciente.nombre} {self.paciente.apellido}"

    class Meta:
        verbose_name_plural = "Planificación Familiar"




class ControlEndocrino(models.Model):
    # Identificación
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha_atencion = models.DateField(auto_now_add=True)
    sede_tratamiento = models.CharField(max_length=150, default="CDI El Llanito", verbose_name="Sede de Tratamiento")
    pas = models.CharField(max_length=10, choices=[('Primera', 'Primera'), ('Sucesiva', 'Sucesiva')], default='Primera', verbose_name="P.A.S.")

    # Signos Vitales
    tension_arterial = models.CharField(max_length=20, null=True, blank=True)
    frecuencia_cardiaca = models.IntegerField(null=True, blank=True)
    frecuencia_respiratoria = models.IntegerField(null=True, blank=True)
    temperatura = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    peso_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    talla_cm = models.IntegerField(null=True, blank=True)
    glucemia_ayunas = models.IntegerField(null=True, blank=True)
    
    # Laboratorios
    hba1c = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    creatinina = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    urea = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    tgo = models.IntegerField(null=True, blank=True)
    tgp = models.IntegerField(null=True, blank=True)
    colesterol_total = models.IntegerField(null=True, blank=True)
    trigliceridos = models.IntegerField(null=True, blank=True)

    # Patologías EXACTAS del Control Operativo Regional (Booleanos puros)
    asociacion_cv = models.BooleanField(default=False, verbose_name="Asociación C.V.")
    insulina = models.BooleanField(default=False, verbose_name="Insulina")
    enfermedad_renal_cronica = models.BooleanField(default=False, verbose_name="Enfermedad Renal Crónica")
    obesidad = models.BooleanField(default=False, verbose_name="Obesidad")
    diabetes_mellitus = models.BooleanField(default=False, verbose_name="Diabetes Mellitus")
    enf_tiroidea = models.BooleanField(default=False, verbose_name="Enf. Tiroidea")
    sobre_peso = models.BooleanField(default=False, verbose_name="Sobre Peso")
    pie_diabetico = models.BooleanField(default=False, verbose_name="Pie Diabético")
    dislipidemia = models.BooleanField(default=False, verbose_name="Dislipidemia")
    
    # Resolución y Otros
    medicamentos_entregados = models.TextField(null=True, blank=True)
    referencia = models.CharField(max_length=200, null=True, blank=True)
    conducta = models.TextField(null=True, blank=True)
    diagnostico = models.TextField(null=True, blank=True)
    tratamiento = models.TextField(null=True, blank=True)
    otras_patologias = models.TextField(null=True, blank=True)
    alergias = models.TextField(null=True, blank=True)
    observaciones_finales = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Control Endocrino - {self.paciente.nombre} {self.paciente.apellido} ({self.fecha_atencion})"


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




    
