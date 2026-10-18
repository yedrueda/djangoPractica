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
    carnet_de_la_patria = models.BooleanField(default=False, verbose_name="Carnet de la Patria")
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

    class Meta:
        verbose_name_plural = "Controles Endocrinos"


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


# --- 5. EJE LOGÍSTICA Y TALENTO HUMANO: TURNOS DE GUARDIA ---
class TurnoGuardia(models.Model):
    TURNOS = [
        ('Diurno 12h', 'Diurno 12h (7:00 AM - 7:00 PM)'),
        ('Nocturno 12h', 'Nocturno 12h (7:00 PM - 7:00 AM)'),
        ('Guardia 24h', 'Guardia 24h (7:00 AM - 7:00 AM)'),
        ('Mañana 6h', 'Mañana (7:00 AM - 1:00 PM)'),
        ('Tarde 6h', 'Tarde (1:00 PM - 7:00 PM)'),
        ('Retén', 'Retén / Disponibilidad'),
    ]

    AREAS = [
        ('Emergencia / Triaje', 'Emergencia / Triaje'),
        ('Hospitalización', 'Hospitalización'),
        ('Terapia Intensiva', 'Terapia Intensiva'),
        ('Enfermería Central', 'Enfermería Central'),
        ('Laboratorio', 'Laboratorio'),
        ('Rayos X / Imagenología', 'Rayos X / Imagenología'),
        ('Farmacia', 'Farmacia'),
        ('Ambulancia / Traslado', 'Ambulancia / Traslado'),
        ('Mantenimiento / Servicios', 'Mantenimiento / Servicios'),
        ('Administración', 'Administración'),
    ]

    ESTADOS = [
        ('Programada', 'Programada'),
        ('En Curso', 'En Curso'),
        ('Cumplida', 'Cumplida'),
        ('Suplida', 'Suplida (Cambio de guardia)'),
        ('Inasistencia', 'Inasistencia'),
    ]

    personal = models.ForeignKey(PersonalCDI, on_delete=models.CASCADE, related_name='guardias', verbose_name="Personal Asignado")
    fecha = models.DateField(verbose_name="Fecha de la Guardia")
    tipo_turno = models.CharField(max_length=50, choices=TURNOS, verbose_name="Tipo de Turno")
    area_servicio = models.CharField(max_length=60, choices=AREAS, verbose_name="Área o Servicio")
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Programada', verbose_name="Estado de la Guardia")
    suplente = models.ForeignKey(PersonalCDI, on_delete=models.SET_NULL, null=True, blank=True, related_name='guardias_suplidas', verbose_name="Personal Suplente (si aplica)")
    observaciones = models.TextField(null=True, blank=True, verbose_name="Observaciones / Novedades")
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fecha} - {self.personal.nombre} {self.personal.apellido} ({self.tipo_turno} en {self.area_servicio})"

    class Meta:
        verbose_name = "Turno de Guardia"
        verbose_name_plural = "Turnos de Guardias"
        ordering = ['-fecha', 'tipo_turno']


# --- 6. EJE TERRITORIAL Y POBLACIONAL (COMUNAS Y CPT) ---
class Comuna(models.Model):
    nombre = models.CharField(max_length=150, unique=True, verbose_name="Nombre de la Comuna")
    orden = models.PositiveIntegerField(default=1, verbose_name="Número / Orden")
    descripcion = models.TextField(null=True, blank=True, verbose_name="Descripción / Ámbito Territorial")

    def __str__(self):
        return f"Comuna {self.orden}: {self.nombre}"

    @property
    def total_poblacion(self):
        return sum(cpt.poblacion for cpt in self.sectores.all())

    @property
    def total_familias(self):
        return sum(cpt.familias for cpt in self.sectores.all())

    class Meta:
        verbose_name = "Comuna"
        verbose_name_plural = "Comunas"
        ordering = ['orden', 'nombre']


class SectorCPT(models.Model):
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE, related_name='sectores', verbose_name="Comuna de Adscripción")
    numero = models.PositiveIntegerField(verbose_name="N° CPT", help_text="Número secuencial en la red del ASIC")
    nombre = models.CharField(max_length=150, verbose_name="Nombre del Sector / Consultorio Popular")
    tipo_cpt = models.CharField(max_length=50, default='CPT 1-2', verbose_name="Clasificación CPT")
    poblacion = models.PositiveIntegerField(default=0, verbose_name="Población Asignada (Habitantes)")
    familias = models.PositiveIntegerField(default=0, verbose_name="Familias Asignadas")
    medico_responsable = models.CharField(max_length=150, null=True, blank=True, verbose_name="Médicos Asignados")
    situacion_espacio = models.CharField(max_length=150, default='Operativo', verbose_name="Situación / Espacio Físico")
    observaciones = models.TextField(null=True, blank=True, verbose_name="Observaciones / Novedades")

    def __str__(self):
        return f"{self.numero}. {self.nombre} ({self.comuna.nombre})"

    class Meta:
        verbose_name = "Consultorio Popular (CPT) / Sector"
        verbose_name_plural = "Consultorios Populares (CPT) / Sectores"
        ordering = ['numero']


class IndicadorPoblacionalASIC(models.Model):
    """Parámetros demográficos y logísticos globales del ASIC (Pizarra oficial)"""
    poblacion_total = models.PositiveIntegerField(default=54975, verbose_name="Población Total")
    familias_total = models.PositiveIntegerField(default=15180, verbose_name="Total Familias")
    comunas_total = models.PositiveIntegerField(default=8, verbose_name="Total Comunas")
    femenino_total = models.PositiveIntegerField(default=28023, verbose_name="Población Femenina (F)")
    masculino_total = models.PositiveIntegerField(default=26952, verbose_name="Población Masculina (M)")
    
    # Puntos de Referencia y Red de Salud (Punto y Círculo)
    red_referencia = models.TextField(
        default="CEO, Hospital Dr. Domingo Luciani, Clínica Popular Mesuca, CPT3 El Carmen",
        verbose_name="Red de Referencia / Punto y Círculo"
    )
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Censo ASIC El Llanito: {self.poblacion_total:,} hab | {self.familias_total:,} familias"

    class Meta:
        verbose_name = "Indicador Demográfico del ASIC"
        verbose_name_plural = "Indicadores Demográficos del ASIC"


