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


# --- 2. EJE PACIENTES (PADRÓN Y FICHA DE ADMISIÓN CLÍNICA) ---
class Paciente(models.Model):
    TIPO_DOC = [
        ('V', 'Venezolano(a)'),
        ('E', 'Extranjero(a)'),
        ('P', 'Pasaporte'),
        ('M', 'Menor sin cédula (Cédula del Representante)'),
    ]
    SEXO = [('M', 'Masculino'), ('F', 'Femenino')]
    ESTADO_CIVIL = [
        ('Soltero(a)', 'Soltero(a)'),
        ('Casado(a)', 'Casado(a)'),
        ('Unión Libre / Concubinato', 'Unión Libre / Concubinato'),
        ('Divorciado(a)', 'Divorciado(a)'),
        ('Viudo(a)', 'Viudo(a)'),
    ]
    GRUPOS_SANGUINEOS = [
        ('Desconocido', 'Desconocido / Por tipificar'),
        ('O+', 'O Rh+'),
        ('O-', 'O Rh-'),
        ('A+', 'A Rh+'),
        ('A-', 'A Rh-'),
        ('B+', 'B Rh+'),
        ('B-', 'B Rh-'),
        ('AB+', 'AB Rh+'),
        ('AB-', 'AB Rh-'),
    ]
    PARENTESCOS = [
        ('Madre / Padre', 'Madre / Padre'),
        ('Esposo(a) / Pareja', 'Esposo(a) / Pareja'),
        ('Hijo(a)', 'Hijo(a)'),
        ('Hermano(a)', 'Hermano(a)'),
        ('Abuelo(a)', 'Abuelo(a)'),
        ('Vecino(a) / Otro', 'Vecino(a) / Otro'),
    ]

    # 1. Identificación y Datos Sociodemográficos
    tipo_cedula = models.CharField(max_length=1, choices=TIPO_DOC, default='V', verbose_name="Tipo Doc.")
    cedula = models.IntegerField(primary_key=True, verbose_name="Cédula de Identidad")
    nombre = models.CharField(max_length=100, verbose_name="Nombres")
    apellido = models.CharField(max_length=100, verbose_name="Apellidos")
    fecha_nacimiento = models.DateField(verbose_name="Fecha de Nacimiento")
    sexo = models.CharField(max_length=1, choices=SEXO, verbose_name="Sexo")
    estado_civil = models.CharField(max_length=30, choices=ESTADO_CIVIL, default='Soltero(a)', verbose_name="Estado Civil")
    ocupacion = models.CharField(max_length=100, null=True, blank=True, verbose_name="Ocupación / Oficio")
    telefono = models.CharField(max_length=20, null=True, blank=True, verbose_name="Teléfono de Contacto")
    correo = models.EmailField(null=True, blank=True, verbose_name="Correo Electrónico")
    carnet_de_la_patria = models.BooleanField(default=False, verbose_name="Posee Carnet de la Patria")

    # 2. Adscripción Territorial (Punto y Círculo ASIC El Llanito)
    asic = models.CharField(max_length=100, default='ASIC El Llanito', verbose_name="ASIC de Adscripción")
    municipio = models.CharField(max_length=100, default='Sucre', verbose_name="Municipio")
    parroquia = models.CharField(max_length=100, default='Petare', verbose_name="Parroquia")
    comuna = models.ForeignKey('Comuna', on_delete=models.SET_NULL, null=True, blank=True, related_name='pacientes', verbose_name="Comuna")
    sector_cpt = models.ForeignKey('SectorCPT', on_delete=models.SET_NULL, null=True, blank=True, related_name='pacientes', verbose_name="Consultorio Popular (CPT) / Sector")
    direccion = models.CharField(max_length=255, verbose_name="Dirección de Habitación / Punto de Referencia")

    # 3. Contacto de Emergencia / Familiar Responsable
    contacto_emergencia_nombre = models.CharField(max_length=150, null=True, blank=True, verbose_name="Contacto de Emergencia (Nombre)")
    contacto_emergencia_parentesco = models.CharField(max_length=40, choices=PARENTESCOS, null=True, blank=True, verbose_name="Parentesco")
    contacto_emergencia_telefono = models.CharField(max_length=20, null=True, blank=True, verbose_name="Teléfono de Emergencia")

    # 4. Perfil Clínico Base y Alertas de Triaje
    grupo_sanguineo = models.CharField(max_length=20, choices=GRUPOS_SANGUINEOS, default='Desconocido', verbose_name="Grupo Sanguíneo y Factor Rh")
    alergias = models.TextField(null=True, blank=True, default='Ninguna conocida', verbose_name="Alergias Medicamentosas / Alimentarias")
    antecedentes_personales = models.TextField(null=True, blank=True, verbose_name="Antecedentes Patológicos Personales (HTA, Diabetes, Asma, Cirugías)")
    antecedentes_familiares = models.TextField(null=True, blank=True, verbose_name="Antecedentes Familiares")
    posee_discapacidad = models.BooleanField(default=False, verbose_name="Posee Alguna Discapacidad")
    detalle_discapacidad = models.CharField(max_length=150, null=True, blank=True, verbose_name="Tipo / Detalle de Discapacidad")
    gestante = models.BooleanField(default=False, verbose_name="Paciente Gestante (Embarazada)")

    fecha_registro = models.DateTimeField(auto_now_add=True)

    @property
    def edad_anios(self) -> int:
        if self.fecha_nacimiento:
            hoy = date.today()
            return hoy.year - self.fecha_nacimiento.year - ((hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))
        return 0

    @property
    def edad(self) -> str:
        if self.fecha_nacimiento:
            return f"{self.edad_anios} años"
        return "Sin registro"

    @property
    def es_adulto_mayor(self) -> bool:
        return self.edad_anios >= 60

    @property
    def prioridad_sugerida_triaje(self) -> str:
        if self.es_adulto_mayor or self.gestante or self.posee_discapacidad:
            return "Prioritario"
        return "Normal"

    def __str__(self):
        return f"{self.tipo_cedula}-{self.cedula} - {self.nombre} {self.apellido}"

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Padrón de Pacientes"
        ordering = ['-fecha_registro']
        indexes = [
            models.Index(fields=['apellido', 'nombre'], name='idx_paciente_nombre_completo'),
            models.Index(fields=['fecha_nacimiento'], name='idx_paciente_fecha_nac'),
            models.Index(fields=['comuna', 'sector_cpt'], name='idx_paciente_territorio'),
        ]


class Turno(models.Model):
    """Cola de Turnos de Atención de Pacientes"""
    PROGRAMAS = [
        ('Triaje General', 'Triaje / Consulta General'),
        ('Endocrino-Metabólico', 'Programa Endocrino-Metabólico'),
        ('Salud Respiratoria', 'Programa de Salud Respiratoria'),
        ('Ruta Materna', 'Programa Ruta Materna'),
        ('Educación Sexual', 'Programa Educación Sexual / Planificación Familiar'),
        ('Emergencia', 'Emergencia'),
    ]
    PRIORIDADES = [
        ('Normal', 'Normal'),
        ('Prioritario', 'Prioritario (Adulto Mayor / Embarazada / Discapacidad)'),
        ('Urgente', 'Urgente'),
    ]
    ESTADOS = [
        ('En Espera', 'En Espera'),
        ('Llamado', 'Llamado a Consulta'),
        ('En Atención', 'En Atención'),
        ('Atendido', 'Atendido'),
        ('Cancelado', 'Cancelado / Ausente'),
    ]

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='turnos')
    codigo_turno = models.CharField(max_length=20, verbose_name="Código de Turno", help_text="Ej: END-001, RESP-002")
    programa = models.CharField(max_length=50, choices=PROGRAMAS, default='Triaje General')
    prioridad = models.CharField(max_length=20, choices=PRIORIDADES, default='Normal')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='En Espera')
    atendido_por = models.ForeignKey(PersonalCDI, on_delete=models.SET_NULL, null=True, blank=True, related_name='turnos_atendidos')
    fecha_hora_llegada = models.DateTimeField(auto_now_add=True)
    fecha_hora_atencion = models.DateTimeField(null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Turno {self.codigo_turno} - {self.paciente.nombre} {self.paciente.apellido} ({self.estado})"

    class Meta:
        verbose_name = "Turno de Atención"
        verbose_name_plural = "Cola de Turnos"
        ordering = ['fecha_hora_llegada']


# --- 3. PROGRAMAS DE SALUD ---
class RutaMaterna(models.Model):
    """Programa Nacional de Parto Humanizado y Ruta Materna (Control Prenatal - CDI El Llanito)"""
    NIVELES_RIESGO_OBSTETRICO = [
        ('Bajo Riesgo (ARO I)', 'Bajo Riesgo Obstétrico (ARO I)'),
        ('Alto Riesgo (ARO II)', 'Alto Riesgo Obstétrico (ARO II)'),
        ('Riesgo Inminente (ARO III)', 'Riesgo Inminente / Emergencia Obstétrica (ARO III)'),
    ]
    MOVIMIENTOS_FETALES = [
        ('Presentes / Normales', 'Presentes y Normales'),
        ('Disminuidos (Alerta)', 'Disminuidos (Signo de Alarma)'),
        ('No evaluable (<18 sem)', 'No evaluable por edad gestacional (<18 sem)'),
        ('Ausentes', 'Ausentes (Urgencia Obstétrica)'),
    ]
    PRESENTACION_FETAL = [
        ('Cefálica', 'Cefálica'),
        ('Podálica', 'Podálica / Pelviana'),
        ('Transversa', 'Situación Transversa'),
        ('Indiferente (<28 sem)', 'Indiferente (<28 semanas)'),
    ]
    SEROLOGIA_ESTATUS = [
        ('No Reactivo', 'No Reactivo (Negativo)'),
        ('Reactivo', 'Reactivo (Positivo - Activar Protocolo)'),
        ('Pendiente', 'Pendiente por Laboratorio'),
    ]

    # 1. Identificación y Control Operativo Prenatal
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    atendido_por = models.ForeignKey(PersonalCDI, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Médico / Obstetra Tratante")
    fecha_control = models.DateField(auto_now_add=True)
    pas = models.CharField(max_length=15, choices=[('Primera', 'Captación / Primera Vez'), ('Sucesiva', 'Control Sucesivo')], default='Primera', verbose_name="Tipo de Captación (P.A.S.)")
    numero_control_prenatal = models.PositiveIntegerField(default=1, verbose_name="N° de Control Prenatal")
    eje = models.CharField(max_length=100, default='ASIC El Llanito', verbose_name="Eje Comunitario / CPT")
    direccion_detallada = models.TextField(null=True, blank=True, verbose_name="Dirección Detallada / Punto de Referencia")

    # 2. Edad Gestacional y Antecedentes Obstétricos (Fórmula G-P-C-A)
    fum = models.DateField(null=True, blank=True, verbose_name="Fecha de Última Menstruación (FUM)")
    fpp = models.DateField(null=True, blank=True, verbose_name="Fecha Probable de Parto (FPP)")
    semanas_embarazo = models.IntegerField(verbose_name="Semanas de Gestación")
    gestas = models.PositiveIntegerField(default=1, verbose_name="Gestas (G)")
    paras = models.PositiveIntegerField(default=0, verbose_name="Partos Vaginales (P)")
    cesareas = models.PositiveIntegerField(default=0, verbose_name="Cesáreas Previas (C)")
    abortos = models.PositiveIntegerField(default=0, verbose_name="Abortos (A)")

    # 3. Evaluación Materno-Fetal y Signos Vitales
    tension_arterial = models.CharField(max_length=20, null=True, blank=True, verbose_name="Tensión Arterial (mmHg)")
    peso_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Peso Materno Actual (Kg)")
    talla_cm = models.PositiveIntegerField(null=True, blank=True, verbose_name="Talla Materna (cm)")
    altura_uterina_cm = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, verbose_name="Altura Uterina (cm)")
    frecuencia_cardiaca_fetal = models.PositiveIntegerField(null=True, blank=True, verbose_name="Frecuencia Cardíaca Fetal - FCF (lpm)")
    movimientos_fetales = models.CharField(max_length=30, choices=MOVIMIENTOS_FETALES, default='Presentes / Normales', verbose_name="Movimientos Fetales")
    presentacion_fetal = models.CharField(max_length=25, choices=PRESENTACION_FETAL, default='Indiferente (<28 sem)', verbose_name="Presentación Fetal")
    edema_miembros_inferiores = models.BooleanField(default=False, verbose_name="Edema en Miembros Inferiores")

    # 4. Paraclínicos, Inmunización y Micronutrientes
    hemoglobina = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, verbose_name="Hemoglobina Materna (g/dL)")
    glucemia_ayunas = models.PositiveIntegerField(null=True, blank=True, verbose_name="Glicemia en Ayunas (mg/dL)")
    vdrl_estatus = models.CharField(max_length=20, choices=SEROLOGIA_ESTATUS, default='Pendiente', verbose_name="Serología VDRL / Sífilis")
    vih_estatus = models.CharField(max_length=20, choices=SEROLOGIA_ESTATUS, default='Pendiente', verbose_name="Prueba Rápida VIH")
    infeccion_urinaria = models.BooleanField(default=False, verbose_name="Infección Urinaria / Bacteriuria")
    toxoide_tetanico = models.BooleanField(default=False, verbose_name="Toxoide Tetánico / dTpa al Día")
    acido_folico_entregado = models.BooleanField(default=True, verbose_name="Entrega de Ácido Fólico")
    sulfato_ferroso_entregado = models.BooleanField(default=True, verbose_name="Entrega de Sulfato Ferroso")
    polivitaminicos_entregados = models.BooleanField(default=False, verbose_name="Entrega de Polivitamínicos Prenatales")

    # 5. Estratificación de Riesgo y Resolución
    riesgo_obstetrico = models.CharField(max_length=30, choices=NIVELES_RIESGO_OBSTETRICO, default='Bajo Riesgo (ARO I)', verbose_name="Clasificación de Riesgo Obstétrico")
    signos_alarma = models.TextField(null=True, blank=True, verbose_name="Signos de Alarma (Sangrado, Cefalea, Tinnitus, Pérdida de Líquido)")
    centro_parto_programado = models.CharField(max_length=150, default="Hospital Dr. Domingo Luciani", verbose_name="Centro Obstétrico de Referencia para el Parto")
    diagnostico = models.TextField(null=True, blank=True, verbose_name="Diagnóstico Obstétrico Integral")
    tratamiento = models.TextField(null=True, blank=True, verbose_name="Indicaciones Médicas y Suplementación")
    observaciones = models.TextField(null=True, blank=True, verbose_name="Observaciones / Plan de Parto Humanizado")
    proxima_cita = models.DateField(null=True, blank=True, verbose_name="Próximo Control Prenatal")

    @property
    def trimestre(self) -> str:
        if self.semanas_embarazo <= 13:
            return "1er Trimestre (1 - 13 sem)"
        if self.semanas_embarazo <= 27:
            return "2do Trimestre (14 - 27 sem)"
        return "3er Trimestre (28 - 42 sem)"

    @property
    def formula_obstetrica(self) -> str:
        return f"G{self.gestas} P{self.paras} C{self.cesareas} A{self.abortos}"

    def __str__(self):
        return f"Ruta Materna - {self.paciente.nombre} {self.paciente.apellido} ({self.semanas_embarazo} sem)"

    class Meta:
        verbose_name = "Control de Ruta Materna"
        verbose_name_plural = "Ruta Materna"
        ordering = ['-fecha_control']


class PlanificacionFamiliar(models.Model):
    """Programa de Educación Sexual, Salud Reproductiva y Planificación Familiar"""
    METODOS_ANTICONCEPTIVOS = [
        ('Solo Consejería', 'Orientación / Consejería en Salud Sexual'),
        ('Preservativos (Barrera)', 'Método de Barrera (Preservativos Masculinos/Femeninos)'),
        ('Oral Combinado (ACO)', 'Anticonceptivo Oral Combinado (Píldoras)'),
        ('Oral Progestágeno (Lactancia)', 'Píldora de Progestágeno Solo (Lactancia)'),
        ('Inyectable Mensual / Trimestral', 'Anticonceptivo Hormonal Inyectable'),
        ('Implante Subdérmico', 'Implante Subdérmico (Implanon / Jadelle)'),
        ('DIU (T de Cobre / Hormonal)', 'Dispositivo Intrauterino (DIU)'),
        ('Esterilización Quirúrgica (Referencia)', 'Referencia para Esterilización Quirúrgica'),
    ]
    OPCIONES_PROCEDIMIENTO = [
        ('No', 'No aplica'),
        ('Colocado', 'Colocado en la Consulta'),
        ('Control', 'Control Sucesivo de Método'),
        ('Retirado', 'Retiro de Método'),
    ]

    # 1. Identificación y Control Operativo Regional
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    atendido_por = models.ForeignKey(PersonalCDI, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Profesional de Salud")
    fecha_atencion = models.DateField(auto_now_add=True)
    semana = models.IntegerField(null=True, blank=True, verbose_name="Semana Epidemiológica")
    primera_sucesiva = models.CharField(max_length=20, choices=[('Primera', 'Primera Vez'), ('Sucesiva', 'Sucesiva')], default='Primera', verbose_name="P.A.S.")
    establecimiento_salud = models.CharField(max_length=100, default='CDI El Llanito', verbose_name="Establecimiento de Salud")
    municipio = models.CharField(max_length=100, default='Sucre', verbose_name="Municipio")

    # 2. Signos Vitales y Valoración Gineco-Reproductiva
    tension_arterial = models.CharField(max_length=20, null=True, blank=True, verbose_name="Tensión Arterial (mmHg)")
    peso_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Peso (Kg)")
    fum = models.DateField(null=True, blank=True, verbose_name="Fecha de Última Menstruación (FUM)")
    prueba_embarazo = models.CharField(
        max_length=25,
        choices=[('No aplica', 'No aplica'), ('Negativa', 'Negativa (-)'), ('Positiva', 'Positiva (+ Derivar a Ruta Materna)')],
        default='No aplica',
        verbose_name="Prueba de Embarazo Previa"
    )

    # 3. Métodos Anticonceptivos y de Barrera Dispensados
    tipo_metodo = models.CharField(max_length=45, choices=METODOS_ANTICONCEPTIVOS, default='Preservativos (Barrera)', verbose_name="Categoría de Método Elegido")
    metodo_entregado = models.CharField(max_length=150, null=True, blank=True, verbose_name="Especificación / Lote de Insumo Entregado")
    preservativo_masculino = models.IntegerField(default=0, verbose_name="Preservativos Masculinos Entregados (Unid.)")
    preservativo_femenino = models.PositiveIntegerField(default=0, verbose_name="Preservativos Femeninos Entregados (Unid.)")
    blister_orales_entregados = models.PositiveIntegerField(default=0, verbose_name="Blísteres / Ciclos Orales Entregados")
    ampollas_inyectables = models.PositiveIntegerField(default=0, verbose_name="Ampollas Inyectables Aplicadas")
    diu = models.CharField(max_length=20, choices=OPCIONES_PROCEDIMIENTO, default='No', verbose_name="Dispositivo Intrauterino (DIU)")
    implante = models.CharField(max_length=20, choices=OPCIONES_PROCEDIMIENTO, default='No', verbose_name="Implante Subdérmico")

    # 4. Prevención de ITS, Pesquisa Ginecológica y Educación Sexual
    consejeria_salud_sexual = models.BooleanField(default=True, verbose_name="Consejería en Educación Sexual y Reproductiva")
    prevencion_its_vih = models.BooleanField(default=True, verbose_name="Orientación en Prevención de ITS / VIH")
    citologia_realizada = models.BooleanField(default=False, verbose_name="Toma de Citología Cervical (Papanicolaou)")
    autoexamen_mamario = models.BooleanField(default=True, verbose_name="Examen / Educación en Autoexamen Mamario")
    despistaje_its_solicitado = models.BooleanField(default=False, verbose_name="Solicitud de VDRL / VIH / Exudado")

    # 5. Diagnóstico, Historial y Seguimiento
    antecedente_obstetrico = models.TextField(null=True, blank=True, verbose_name="Antecedentes Gineco-Obstétricos y Uso Previo de Métodos")
    diagnostico = models.TextField(null=True, blank=True, verbose_name="Diagnóstico / Criterio de Elegibilidad OMS")
    observaciones = models.TextField(null=True, blank=True, verbose_name="Observaciones y Acuerdos con el/la Paciente")
    proxima_cita = models.DateField(null=True, blank=True, verbose_name="Fecha de Próximo Control / Reabastecimiento")

    def __str__(self):
        return f"Planificación Familiar - {self.paciente.nombre} {self.paciente.apellido}"

    class Meta:
        verbose_name = "Control de Educación Sexual y Planificación Familiar"
        verbose_name_plural = "Planificación Familiar"
        ordering = ['-fecha_atencion']




class ControlEndocrino(models.Model):
    """Programa de Salud Endocrino-Metabólica (CAREMT - CDI El Llanito)"""
    TIPOS_DIABETES = [
        ('No aplica', 'Sin Diabetes / En Estudio'),
        ('Prediabetes', 'Prediabetes / Glucemia Alterada en Ayunas'),
        ('Tipo 1', 'Diabetes Mellitus Tipo 1 (Insulinodependiente)'),
        ('Tipo 2', 'Diabetes Mellitus Tipo 2'),
        ('Gestacional', 'Diabetes Gestacional'),
    ]
    ESCALA_WAGNER = [
        ('Grado 0', 'Grado 0: Pie de riesgo sin úlcera activa'),
        ('Grado I', 'Grado I: Úlcera superficial de espesor total'),
        ('Grado II', 'Grado II: Úlcera profunda (tendón/cápsula sin osteomielitis)'),
        ('Grado III', 'Grado III: Úlcera profunda con absceso u osteomielitis'),
        ('Grado IV', 'Grado IV: Gangrena localizada (dedos o antepié)'),
        ('Grado V', 'Grado V: Gangrena extensa de todo el pie'),
    ]
    NIVELES_RIESGO_CV = [
        ('Bajo', 'Riesgo Bajo (<10%)'),
        ('Moderado', 'Riesgo Moderado (10% - 20%)'),
        ('Alto', 'Riesgo Alto (20% - 30%)'),
        ('Muy Alto', 'Riesgo Muy Alto (>30% / Evento CV previo)'),
    ]

    # 1. Identificación y Control Operativo
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    atendido_por = models.ForeignKey(PersonalCDI, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Médico Tratante")
    fecha_atencion = models.DateField(auto_now_add=True)
    sede_tratamiento = models.CharField(max_length=150, default="CDI El Llanito", verbose_name="Sede de Tratamiento")
    pas = models.CharField(max_length=10, choices=[('Primera', 'Primera'), ('Sucesiva', 'Sucesiva')], default='Primera', verbose_name="P.A.S.")
    semana_epidemiologica = models.PositiveIntegerField(null=True, blank=True, verbose_name="Semana Epidemiológica")

    # 2. Signos Vitales y Antropometría Metabólica
    tension_arterial = models.CharField(max_length=20, null=True, blank=True, verbose_name="Tensión Arterial (mmHg)")
    frecuencia_cardiaca = models.IntegerField(null=True, blank=True, verbose_name="Frecuencia Cardíaca (lpm)")
    frecuencia_respiratoria = models.IntegerField(null=True, blank=True, verbose_name="Frecuencia Respiratoria (rpm)")
    temperatura = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, verbose_name="Temperatura (°C)")
    peso_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Peso (Kg)")
    talla_cm = models.IntegerField(null=True, blank=True, verbose_name="Talla (cm)")
    circunferencia_abdominal_cm = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, verbose_name="Circunferencia Abdominal (cm)")
    glucemia_ayunas = models.IntegerField(null=True, blank=True, verbose_name="Glicemia en Ayunas (mg/dL)")
    glucemia_postprandial = models.IntegerField(null=True, blank=True, verbose_name="Glicemia Postprandial 2h (mg/dL)")

    # 3. Laboratorios Clínicos y Perfil Tiroideo/Renal/Lipídico
    hba1c = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, verbose_name="HbA1c (%)")
    creatinina = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Creatinina Sérica (mg/dL)")
    urea = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Urea (mg/dL)")
    acido_urico = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, verbose_name="Ácido Úrico (mg/dL)")
    proteinuria_24h = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True, verbose_name="Microalbuminuria / Proteinuria (mg/24h)")
    tgo = models.IntegerField(null=True, blank=True, verbose_name="TGO / AST (U/L)")
    tgp = models.IntegerField(null=True, blank=True, verbose_name="TGP / ALT (U/L)")
    colesterol_total = models.IntegerField(null=True, blank=True, verbose_name="Colesterol Total (mg/dL)")
    colesterol_hdl = models.IntegerField(null=True, blank=True, verbose_name="Colesterol HDL (mg/dL)")
    colesterol_ldl = models.IntegerField(null=True, blank=True, verbose_name="Colesterol LDL (mg/dL)")
    trigliceridos = models.IntegerField(null=True, blank=True, verbose_name="Triglicéridos (mg/dL)")
    tsh = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="TSH (µUI/mL)")
    t4_libre = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name="T4 Libre (ng/dL)")

    # 4. Patologías del Control Operativo Regional (CAREMT) y Estratificación
    asociacion_cv = models.BooleanField(default=False, verbose_name="Asociación C.V.")
    hipertension_arterial = models.BooleanField(default=False, verbose_name="Hipertensión Arterial (HTA)")
    insulina = models.BooleanField(default=False, verbose_name="Uso de Insulina")
    enfermedad_renal_cronica = models.BooleanField(default=False, verbose_name="Enfermedad Renal Crónica")
    obesidad = models.BooleanField(default=False, verbose_name="Obesidad")
    diabetes_mellitus = models.BooleanField(default=False, verbose_name="Diabetes Mellitus")
    enf_tiroidea = models.BooleanField(default=False, verbose_name="Enf. Tiroidea")
    sobre_peso = models.BooleanField(default=False, verbose_name="Sobre Peso")
    pie_diabetico = models.BooleanField(default=False, verbose_name="Pie Diabético")
    dislipidemia = models.BooleanField(default=False, verbose_name="Dislipidemia")

    tipo_diabetes = models.CharField(max_length=25, choices=TIPOS_DIABETES, default='No aplica', verbose_name="Clasificación de Diabetes")
    clasificacion_pie_diabetico = models.CharField(max_length=20, choices=ESCALA_WAGNER, default='Grado 0', verbose_name="Escala de Wagner (Pie Diabético)")
    riesgo_cardiovascular = models.CharField(max_length=20, choices=NIVELES_RIESGO_CV, default='Moderado', verbose_name="Riesgo Cardiovascular Global")

    # 5. Resolución Terapéutica, Insumos y Seguimiento
    esquema_insulina = models.CharField(max_length=150, null=True, blank=True, verbose_name="Esquema de Insulina (Ej: NPH 20 UI AM / 10 UI PM)")
    tiras_reactivas_entregadas = models.PositiveIntegerField(default=0, verbose_name="Tiras Reactivas / Lancetas Entregadas")
    medicamentos_entregados = models.TextField(null=True, blank=True, verbose_name="Medicamentos Dispensados (Farmacia CDI)")
    referencia = models.CharField(max_length=200, null=True, blank=True, verbose_name="Referencia a Especialidad / Red Hospitalaria")
    conducta = models.TextField(null=True, blank=True, verbose_name="Conducta Médica y Educación Diabetológica")
    diagnostico = models.TextField(null=True, blank=True, verbose_name="Diagnóstico Clínico Integral")
    tratamiento = models.TextField(null=True, blank=True, verbose_name="Plan Terapéutico y Posología")
    otras_patologias = models.TextField(null=True, blank=True, verbose_name="Otras Patologías Asociadas")
    alergias = models.TextField(null=True, blank=True, verbose_name="Alergias Reportadas en Consulta")
    observaciones_finales = models.TextField(null=True, blank=True, verbose_name="Observaciones Finales")
    proxima_cita = models.DateField(null=True, blank=True, verbose_name="Fecha de Próximo Control")

    @property
    def imc(self) -> float | None:
        if self.peso_kg and self.talla_cm and self.talla_cm > 0:
            talla_m = float(self.talla_cm) / 100.0
            return round(float(self.peso_kg) / (talla_m ** 2), 2)
        return None

    @property
    def clasificacion_imc(self) -> str:
        valor_imc = self.imc
        if valor_imc is None:
            return "Sin datos antropométricos"
        if valor_imc < 18.5:
            return "Bajo Peso (<18.5)"
        if valor_imc < 25.0:
            return "Normopeso (18.5 - 24.9)"
        if valor_imc < 30.0:
            return "Sobrepeso (25.0 - 29.9)"
        if valor_imc < 35.0:
            return "Obesidad Grado I (30.0 - 34.9)"
        if valor_imc < 40.0:
            return "Obesidad Grado II (35.0 - 39.9)"
        return "Obesidad Grado III / Mórbida (>=40.0)"

    @property
    def estado_control_glucemico(self) -> str:
        if self.glucemia_ayunas is not None and self.glucemia_ayunas < 70:
            return "Alerta: Hipoglucemia (<70 mg/dL)"
        if (self.hba1c is not None and float(self.hba1c) >= 8.5) or (self.glucemia_ayunas is not None and self.glucemia_ayunas >= 180):
            return "Descompensado / Hiperglucemia Severa"
        if (self.hba1c is not None and float(self.hba1c) > 7.0) or (self.glucemia_ayunas is not None and self.glucemia_ayunas > 130):
            return "Control Subóptimo (Requiere ajuste terapéutico)"
        if self.hba1c is not None or self.glucemia_ayunas is not None:
            return "En Meta Terapéutica (Controlado)"
        return "Pendiente de perfil glucémico"

    def __str__(self):
        return f"Control Endocrino - {self.paciente.nombre} {self.paciente.apellido} ({self.fecha_atencion})"

    class Meta:
        verbose_name = "Control Endocrino-Metabólico"
        verbose_name_plural = "Controles Endocrinos"
        ordering = ['-fecha_atencion']


class ControlRespiratorio(models.Model):
    """Programa de Salud Respiratoria y Sala de Terapia Respiratoria (IRA / Asma / EPOC / TB)"""
    SEVERIDADES = [
        ('Estable / Control', 'Cuadro Estable / Control Ambulatorio'),
        ('Leve', 'Exacerbación / Cuadro Agudo Leve'),
        ('Moderado', 'Crisis / Cuadro Moderado (Requiere Terapia en Sala)'),
        ('Severo', 'Crisis Severa / Insuficiencia Respiratoria (Referencia Urgente)'),
    ]
    RESULTADOS_BK = [
        ('No solicitada', 'No aplica / No solicitada'),
        ('Pendiente', 'Muestra tomada - Resultado Pendiente'),
        ('Negativo (-)', 'Baciloscopia Negativa (-)'),
        ('Positivo (+)', 'Positivo (+)'),
        ('Positivo (++)', 'Positivo (++)'),
        ('Positivo (+++)', 'Positivo (+++)'),
    ]

    # 1. Identificación y Control Operativo
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='controles_respiratorios')
    fecha_atencion = models.DateField(auto_now_add=True)
    sede_tratamiento = models.CharField(max_length=150, default="CDI El Llanito", verbose_name="Sede de Tratamiento")
    pas = models.CharField(max_length=10, choices=[('Primera', 'Primera'), ('Sucesiva', 'Sucesiva')], default='Primera', verbose_name="P.A.S.")
    semana_epidemiologica = models.PositiveIntegerField(null=True, blank=True, verbose_name="Semana Epidemiológica")
    atendido_por = models.ForeignKey(PersonalCDI, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Médico Tratante")

    # 2. Signos Vitales, Oximetría y Función Respiratoria
    saturacion_oxigeno = models.PositiveIntegerField(null=True, blank=True, verbose_name="Saturación O2 - SpO2 (%)")
    frecuencia_respiratoria = models.PositiveIntegerField(null=True, blank=True, verbose_name="Frecuencia Respiratoria (rpm)")
    frecuencia_cardiaca = models.PositiveIntegerField(null=True, blank=True, verbose_name="Frecuencia Cardíaca (lpm)")
    temperatura = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, verbose_name="Temperatura (°C)")
    tension_arterial = models.CharField(max_length=20, null=True, blank=True, verbose_name="Tensión Arterial (mmHg)")
    flujo_espiratorio_pico = models.PositiveIntegerField(null=True, blank=True, verbose_name="Flujo Espiratorio Pico (PEF L/min)")
    severidad_cuadro = models.CharField(max_length=25, choices=SEVERIDADES, default='Estable / Control', verbose_name="Severidad Clínica")

    # 3. Cuadro Clínico y Patologías Respiratorias (Booleanos)
    asma_bronquial = models.BooleanField(default=False, verbose_name="Asma Bronquial")
    epoc = models.BooleanField(default=False, verbose_name="EPOC")
    infeccion_respiratoria_aguda = models.BooleanField(default=False, verbose_name="Infección Respiratoria Aguda (IRA)")
    neumonia = models.BooleanField(default=False, verbose_name="Neumonía / Bronconeumonía")
    sospecha_tuberculosis = models.BooleanField(default=False, verbose_name="Sintomático Respiratorio / Sospecha TB")
    rinitis_alergica = models.BooleanField(default=False, verbose_name="Rinitis Alérgica")
    tabaquismo = models.BooleanField(default=False, verbose_name="Antecedente de Tabaquismo / Exposición a Biomasa")

    # 4. Síntomas y Procedimientos en Sala de Terapia Respiratoria (ERA)
    tos_con_expectoracion = models.BooleanField(default=False, verbose_name="Tos con Expectoración (>14 días)")
    disnea = models.BooleanField(default=False, verbose_name="Disnea / Tiraje Intercostal")
    sibilancias = models.BooleanField(default=False, verbose_name="Sibilancias / Roncus a la Auscultación")
    nebulizacion_realizada = models.BooleanField(default=False, verbose_name="Terapia de Nebulización Aplicada en Sala")
    esquema_nebulizacion = models.CharField(max_length=150, null=True, blank=True, verbose_name="Fármaco y Ciclos de Nebulización (Ej: Salbutamol + Ipratropio x 3 ciclos)")
    oxigenoterapia = models.BooleanField(default=False, verbose_name="Oxigenoterapia Aplicada")
    litros_oxigeno_min = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, verbose_name="Flujo de O2 (L/min)")
    baciloscopia_solicitada = models.BooleanField(default=False, verbose_name="Baciloscopia Seriada de Esputo (BK) Solicitada")
    resultado_bk = models.CharField(max_length=20, choices=RESULTADOS_BK, default='No solicitada', verbose_name="Resultado de Baciloscopia (BK)")
    hallazgos_radiografia = models.CharField(max_length=200, null=True, blank=True, verbose_name="Hallazgos en Rx de Tórax")

    # 5. Resolución Clínica y Seguimiento
    diagnostico = models.TextField(null=True, blank=True, verbose_name="Diagnóstico Respiratorio Integral")
    tratamiento = models.TextField(null=True, blank=True, verbose_name="Plan Terapéutico e Inhaloterapia")
    medicamentos_entregados = models.TextField(null=True, blank=True, verbose_name="Inhaladores / Medicamentos Entregados")
    referencia = models.CharField(max_length=200, null=True, blank=True, verbose_name="Referencia a Neumología / Hospital")
    observaciones = models.TextField(null=True, blank=True, verbose_name="Evolución Post-Terapia y Observaciones")
    proxima_cita = models.DateField(null=True, blank=True, verbose_name="Fecha de Próximo Control")

    @property
    def estado_oxigenacion(self) -> str:
        if self.saturacion_oxigeno is None:
            return "Sin registro de SpO2"
        if self.saturacion_oxigeno >= 95:
            return "Normoxemia (>=95%)"
        if self.saturacion_oxigeno >= 91:
            return "Hipoxemia Leve (91% - 94%)"
        return "Alerta: Hipoxemia Moderada/Severa (<=90% - Requiere O2)"

    def __str__(self):
        return f"Control Respiratorio - {self.paciente.nombre} {self.paciente.apellido} ({self.fecha_atencion})"

    class Meta:
        verbose_name = "Control Respiratorio"
        verbose_name_plural = "Controles Respiratorios"
        ordering = ['-fecha_atencion']


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
    def total_poblacion(self) -> int:
        return sum(cpt.poblacion for cpt in self.sectores.all())

    @property
    def total_familias(self) -> int:
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


