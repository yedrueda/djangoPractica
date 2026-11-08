from datetime import date
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from .models import (
    PersonalCDI,
    Paciente,
    Turno,
    RutaMaterna,
    PlanificacionFamiliar,
    ControlEndocrino,
    ControlRespiratorio,
    InventarioEquipo,
    TurnoGuardia,
    Comuna,
    SectorCPT,
    IndicadorPoblacionalASIC,
)


# ==========================================
# 1. EJE DE PERSONAL Y GUARDIAS (RRHH)
# ==========================================
class PersonalCDISerializer(serializers.ModelSerializer):
    nombre_completo = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PersonalCDI
        fields = '__all__'

    def get_nombre_completo(self, obj) -> str:
        return f"{obj.nombre} {obj.apellido}"


class TurnoGuardiaSerializer(serializers.ModelSerializer):
    personal_nombre = serializers.CharField(source='personal.__str__', read_only=True)
    suplente_nombre = serializers.CharField(source='suplente.__str__', read_only=True)

    class Meta:
        model = TurnoGuardia
        fields = '__all__'


# ==========================================
# 2. PADRÓN DE PACIENTES Y COLA DE TURNOS
# ==========================================
@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Admisión de Paciente Nuevo (Caso Real CDI El Llanito)',
            summary='Ficha completa de admisión clínica de un paciente nuevo',
            description='Ejemplo realista de apertura de historia clínica en el CDI El Llanito (ASIC El Llanito, Municipio Sucre).',
            value={
                'tipo_cedula': 'V',
                'cedula': 14852963,
                'nombre': 'María Fernanda',
                'apellido': 'Rojas Pérez',
                'fecha_nacimiento': '1982-05-14',
                'sexo': 'F',
                'estado_civil': 'Casado(a)',
                'ocupacion': 'Docente de Educación Inicial',
                'telefono': '0412-5558912',
                'correo': 'mrojas82@gmail.com',
                'carnet_de_la_patria': True,
                'asic': 'ASIC El Llanito',
                'municipio': 'Sucre',
                'parroquia': 'Petare',
                'comuna': None,
                'sector_cpt': None,
                'direccion': 'Av. Principal de El Llanito, Calle Tamanaco, Res. Los Jabillos, Piso 3 Apto 3-B',
                'contacto_emergencia_nombre': 'Carlos Alberto Gómez',
                'contacto_emergencia_parentesco': 'Esposo(a) / Pareja',
                'contacto_emergencia_telefono': '0414-3216549',
                'grupo_sanguineo': 'O+',
                'alergias': 'Alergia a la Penicilina y Dipirona (AINES)',
                'antecedentes_personales': 'Hipertensión Arterial diagnosticada hace 4 años en tratamiento con Losartán 50mg.',
                'antecedentes_familiares': 'Madre con Diabetes Mellitus Tipo 2, Padre hipertenso.',
                'posee_discapacidad': False,
                'detalle_discapacidad': '',
                'gestante': False,
            },
            request_only=True,
        )
    ]
)
class PacienteSerializer(serializers.ModelSerializer):
    edad = serializers.ReadOnlyField()
    edad_anios = serializers.ReadOnlyField()
    es_adulto_mayor = serializers.ReadOnlyField()
    prioridad_sugerida_triaje = serializers.ReadOnlyField()
    nombre_completo = serializers.SerializerMethodField(read_only=True)
    comuna_nombre = serializers.CharField(source='comuna.nombre', read_only=True)
    sector_cpt_nombre = serializers.CharField(source='sector_cpt.nombre', read_only=True)

    class Meta:
        model = Paciente
        fields = '__all__'

    def get_nombre_completo(self, obj) -> str:
        return f"{obj.nombre} {obj.apellido}"

    def validate_fecha_nacimiento(self, value):
        if value > date.today():
            raise serializers.ValidationError("La fecha de nacimiento no puede ser una fecha futura.")
        return value

    def validate(self, attrs):
        sexo = attrs.get('sexo', getattr(self.instance, 'sexo', None))
        gestante = attrs.get('gestante', getattr(self.instance, 'gestante', False))
        posee_discapacidad = attrs.get('posee_discapacidad', getattr(self.instance, 'posee_discapacidad', False))
        detalle_discapacidad = attrs.get('detalle_discapacidad', getattr(self.instance, 'detalle_discapacidad', ''))

        if gestante and sexo == 'M':
            raise serializers.ValidationError({
                'gestante': 'Un paciente de sexo masculino no puede marcarse como gestante.'
            })
        if posee_discapacidad and not detalle_discapacidad:
            raise serializers.ValidationError({
                'detalle_discapacidad': 'Indique el tipo o detalle de la discapacidad del paciente.'
            })
        return attrs


class TurnoSerializer(serializers.ModelSerializer):
    paciente_nombre = serializers.SerializerMethodField(read_only=True)
    atendido_por_nombre = serializers.CharField(source='atendido_por.__str__', read_only=True)
    codigo_turno = serializers.CharField(max_length=20, required=False, allow_blank=True)

    class Meta:
        model = Turno
        fields = '__all__'

    def get_paciente_nombre(self, obj) -> str:
        return f"{obj.paciente.tipo_cedula}-{obj.paciente.cedula} {obj.paciente.nombre} {obj.paciente.apellido}"

    def create(self, validated_data):
        paciente = validated_data.get('paciente')
        programa = validated_data.get('programa', 'Triaje General')

        # Si no se especificó prioridad y el paciente tiene condición prioritaria, asignarla automáticamente
        if 'prioridad' not in validated_data and paciente:
            validated_data['prioridad'] = paciente.prioridad_sugerida_triaje

        # Autogenerar código de turno secuencial del día si no se envió uno
        if not validated_data.get('codigo_turno'):
            prefijos = {
                'Triaje General': 'TRJ',
                'Endocrino-Metabólico': 'END',
                'Salud Respiratoria': 'RESP',
                'Ruta Materna': 'MAT',
                'Educación Sexual': 'ESX',
                'Emergencia': 'EMG',
            }
            prefijo = prefijos.get(programa, 'CDI')
            hoy = date.today()
            correlativo = Turno.objects.filter(fecha_hora_llegada__date=hoy, programa=programa).count() + 1
            validated_data['codigo_turno'] = f"{prefijo}-{correlativo:03d}"

        return super().create(validated_data)


# ==========================================
# 3. LOS 4 PROGRAMAS DE SALUD AUTORIZADOS
# ==========================================
@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Evaluación Endocrino-Metabólica (Caso Real CAREMT - CDI El Llanito)',
            summary='Control clínico de paciente con Diabetes Tipo 2, HTA y Dislipidemia',
            description=(
                'Caso real del Programa Endocrino-Metabólico / Buen Vivir para el Diabético en el CDI El Llanito: '
                'Paciente con DM Tipo 2 en control sucesivo, evaluación antropométrica, perfil lipídico/renal/tiroideo '
                'y entrega de medicamentos e insumos.'
            ),
            value={
                'paciente': 14852963,
                'atendido_por': None,
                'sede_tratamiento': 'CDI El Llanito',
                'pas': 'Sucesiva',
                'semana_epidemiologica': 45,
                'tension_arterial': '135/85',
                'frecuencia_cardiaca': 78,
                'frecuencia_respiratoria': 18,
                'temperatura': '36.6',
                'peso_kg': '82.50',
                'talla_cm': 162,
                'circunferencia_abdominal_cm': '96.5',
                'glucemia_ayunas': 158,
                'glucemia_postprandial': 210,
                'hba1c': '7.8',
                'creatinina': '1.05',
                'urea': '34.0',
                'acido_urico': '5.8',
                'proteinuria_24h': '45.0',
                'tgo': 28,
                'tgp': 32,
                'colesterol_total': 224,
                'colesterol_hdl': 42,
                'colesterol_ldl': 138,
                'trigliceridos': 220,
                'tsh': '2.45',
                't4_libre': '1.15',
                'asociacion_cv': True,
                'hipertension_arterial': True,
                'insulina': True,
                'enfermedad_renal_cronica': False,
                'obesidad': True,
                'diabetes_mellitus': True,
                'enf_tiroidea': False,
                'sobre_peso': False,
                'pie_diabetico': False,
                'dislipidemia': True,
                'tipo_diabetes': 'Tipo 2',
                'clasificacion_pie_diabetico': 'Grado 0',
                'riesgo_cardiovascular': 'Alto',
                'esquema_insulina': 'Insulina NPH 18 UI SC 7:00 AM y 10 UI SC 9:00 PM',
                'tiras_reactivas_entregadas': 50,
                'medicamentos_entregados': 'Metformina 850mg (#60 tab), Losartán Potásico 50mg (#30 tab), Atorvastatina 20mg (#30 tab), Insulina NPH 100 UI/mL (1 vial)',
                'referencia': 'Valoración anual por Oftalmología (Fondo de ojo) y Nutrición',
                'conducta': 'Se refuerza educación diabetológica, plan nutricional hipoglúcido/hiposódico, caminata 30 min/día y revisión diaria de pies.',
                'diagnostico': '1. Diabetes Mellitus Tipo 2 en control subóptimo (HbA1c 7.8%). 2. Hipertensión Arterial Estadio 1. 3. Obesidad Grado I (IMC 31.44 kg/m2). 4. Dislipidemia mixta.',
                'tratamiento': '1. Insulina NPH 18 UI AM / 10 UI PM. 2. Metformina 850mg VO con desayuno y cena. 3. Losartán 50mg VO c/12h. 4. Atorvastatina 20mg VO 9:00 PM.',
                'otras_patologias': 'Insuficiencia venosa periférica leve en miembros inferiores.',
                'alergias': 'Alergia a la Penicilina y Dipirona (AINES)',
                'observaciones_finales': 'Paciente acude con bitácora de automonitoreo capilar. Sin lesiones en miembros inferiores (Wagner 0).',
                'proxima_cita': '2026-12-08',
            },
            request_only=True,
        )
    ]
)
class ControlEndocrinoSerializer(serializers.ModelSerializer):
    paciente_nombre = serializers.SerializerMethodField(read_only=True)
    atendido_por_nombre = serializers.CharField(source='atendido_por.__str__', read_only=True)
    imc = serializers.ReadOnlyField()
    clasificacion_imc = serializers.ReadOnlyField()
    estado_control_glucemico = serializers.ReadOnlyField()

    class Meta:
        model = ControlEndocrino
        fields = '__all__'

    def get_paciente_nombre(self, obj) -> str:
        return f"{obj.paciente.tipo_cedula}-{obj.paciente.cedula} {obj.paciente.nombre} {obj.paciente.apellido}"

    def validate(self, attrs):
        peso = attrs.get('peso_kg', getattr(self.instance, 'peso_kg', None))
        talla = attrs.get('talla_cm', getattr(self.instance, 'talla_cm', None))
        if peso and talla and talla > 0:
            imc_calc = float(peso) / ((float(talla) / 100.0) ** 2)
            # Autocompletar banderas epidemiológicas de sobrepeso/obesidad si no fueron enviadas explícitamente
            if 'obesidad' not in attrs and 'sobre_peso' not in attrs:
                if imc_calc >= 30.0:
                    attrs['obesidad'] = True
                    attrs['sobre_peso'] = False
                elif 25.0 <= imc_calc < 30.0:
                    attrs['sobre_peso'] = True
                    attrs['obesidad'] = False
        return attrs


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Evaluación de Salud Respiratoria (Caso Real Sala de Terapia Respiratoria CDI)',
            summary='Paciente con crisis asmática moderada e IRA atendido en nebulización',
            value={
                'paciente': 14852963,
                'atendido_por': None,
                'sede_tratamiento': 'CDI El Llanito',
                'pas': 'Primera',
                'semana_epidemiologica': 45,
                'saturacion_oxigeno': 93,
                'frecuencia_respiratoria': 24,
                'frecuencia_cardiaca': 96,
                'temperatura': '37.4',
                'tension_arterial': '125/80',
                'flujo_espiratorio_pico': 310,
                'severidad_cuadro': 'Moderado',
                'asma_bronquial': True,
                'epoc': False,
                'infeccion_respiratoria_aguda': True,
                'neumonia': False,
                'sospecha_tuberculosis': False,
                'rinitis_alergica': True,
                'tabaquismo': False,
                'tos_con_expectoracion': False,
                'disnea': True,
                'sibilancias': True,
                'nebulizacion_realizada': True,
                'esquema_nebulizacion': 'Salbutamol 15 gotas + Bromuro de Ipratropio 10 gotas en 3 cc Sol. 0.9% (3 ciclos c/20 min)',
                'oxigenoterapia': False,
                'litros_oxigeno_min': None,
                'baciloscopia_solicitada': False,
                'resultado_bk': 'No solicitada',
                'hallazgos_radiografia': 'Atrapamiento aéreo bilateral sin consolidaciones neumónicas.',
                'diagnostico': 'Crisis aguda de Asma Bronquial moderada desencadenada por Infección Respiratoria Aguda alta.',
                'tratamiento': 'Salbutamol inhalador 2 puff c/6h por 7 días, Prednisona 50mg VO OD por 5 días, Loratadina 10mg VO OD.',
                'medicamentos_entregados': 'Salbutamol inhalador 100mcg (1 unidad), Prednisona 50mg (#5 tab), Loratadina 10mg (#10 tab)',
                'referencia': 'Control por consulta de Salud Respiratoria en 7 días',
                'observaciones': 'Saturación de O2 mejora de 93% a 98% tras esquema de nebulización en sala.',
                'proxima_cita': '2026-11-15',
            },
            request_only=True,
        )
    ]
)
class ControlRespiratorioSerializer(serializers.ModelSerializer):
    paciente_nombre = serializers.SerializerMethodField(read_only=True)
    atendido_por_nombre = serializers.CharField(source='atendido_por.__str__', read_only=True)
    estado_oxigenacion = serializers.ReadOnlyField()

    class Meta:
        model = ControlRespiratorio
        fields = '__all__'

    def get_paciente_nombre(self, obj) -> str:
        return f"{obj.paciente.tipo_cedula}-{obj.paciente.cedula} {obj.paciente.nombre} {obj.paciente.apellido}"


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Control Prenatal - Ruta Materna (Caso Real CDI El Llanito)',
            summary='Control prenatal de gestante de 24 semanas (2do Trimestre)',
            value={
                'paciente': 14852963,
                'atendido_por': None,
                'pas': 'Sucesiva',
                'numero_control_prenatal': 4,
                'eje': 'Comuna 1 - CPT El Llanito',
                'direccion_detallada': 'Av. Principal de El Llanito, Calle Tamanaco, Res. Los Jabillos',
                'fum': '2026-05-24',
                'fpp': '2027-02-28',
                'semanas_embarazo': 24,
                'gestas': 2,
                'paras': 1,
                'cesareas': 0,
                'abortos': 0,
                'tension_arterial': '110/70',
                'peso_kg': '66.40',
                'talla_cm': 162,
                'altura_uterina_cm': '23.0',
                'frecuencia_cardiaca_fetal': 144,
                'movimientos_fetales': 'Presentes / Normales',
                'presentacion_fetal': 'Cefálica',
                'edema_miembros_inferiores': False,
                'hemoglobina': '11.8',
                'glucemia_ayunas': 84,
                'vdrl_estatus': 'No Reactivo',
                'vih_estatus': 'No Reactivo',
                'infeccion_urinaria': False,
                'toxoide_tetanico': True,
                'acido_folico_entregado': True,
                'sulfato_ferroso_entregado': True,
                'polivitaminicos_entregados': True,
                'riesgo_obstetrico': 'Bajo Riesgo (ARO I)',
                'signos_alarma': 'Niega sangrado genital, cefalea, fosfenos o pérdida de líquido amniótico.',
                'centro_parto_programado': 'Hospital Dr. Domingo Luciani',
                'diagnostico': '1. Embarazo simple de 24 semanas por FUM. 2. Bajo Riesgo Obstétrico (ARO I) normoevolutivo.',
                'tratamiento': 'Sulfato Ferroso 300mg VO OD, Ácido Fólico 5mg VO OD, Calcio 600mg VO OD.',
                'observaciones': 'Se orienta sobre signos de alarma obstétrica, lactancia materna exclusiva y ejercicios de psicoprofilaxis.',
                'proxima_cita': '2026-12-06',
            },
            request_only=True,
        )
    ]
)
class RutaMaternaSerializer(serializers.ModelSerializer):
    paciente_nombre = serializers.SerializerMethodField(read_only=True)
    atendido_por_nombre = serializers.CharField(source='atendido_por.__str__', read_only=True)
    trimestre = serializers.ReadOnlyField()
    formula_obstetrica = serializers.ReadOnlyField()

    class Meta:
        model = RutaMaterna
        fields = '__all__'

    def get_paciente_nombre(self, obj) -> str:
        return f"{obj.paciente.tipo_cedula}-{obj.paciente.cedula} {obj.paciente.nombre} {obj.paciente.apellido}"


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Educación Sexual y Planificación Familiar (Caso Real CDI El Llanito)',
            summary='Orientación anticonceptiva, pesquisa ginecológica y entrega de métodos',
            value={
                'paciente': 14852963,
                'atendido_por': None,
                'semana': 45,
                'primera_sucesiva': 'Primera',
                'establecimiento_salud': 'CDI El Llanito',
                'municipio': 'Sucre',
                'tension_arterial': '118/76',
                'peso_kg': '62.00',
                'fum': '2026-10-28',
                'prueba_embarazo': 'Negativa',
                'tipo_metodo': 'Oral Combinado (ACO)',
                'metodo_entregado': 'Levonorgestrel 0.15mg / Etinilestradiol 0.03mg (3 blísteres) + 12 preservativos',
                'preservativo_masculino': 12,
                'preservativo_femenino': 0,
                'blister_orales_entregados': 3,
                'ampollas_inyectables': 0,
                'diu': 'No',
                'implante': 'No',
                'consejeria_salud_sexual': True,
                'prevencion_its_vih': True,
                'citologia_realizada': True,
                'autoexamen_mamario': True,
                'despistaje_its_solicitado': True,
                'antecedente_obstetrico': 'Menarquia 12 años, ciclos regulares 28/4. II Gestas, II Paras, 0 Abortos.',
                'diagnostico': 'Usuaria sana en edad reproductiva (Categoría 1 Criterios de Elegibilidad Médica OMS para ACO).',
                'observaciones': 'Se realiza toma de citología cervical, educación en doble protección y técnica de autoexamen mamario.',
                'proxima_cita': '2027-02-08',
            },
            request_only=True,
        )
    ]
)
class PlanificacionFamiliarSerializer(serializers.ModelSerializer):
    paciente_nombre = serializers.SerializerMethodField(read_only=True)
    atendido_por_nombre = serializers.CharField(source='atendido_por.__str__', read_only=True)

    class Meta:
        model = PlanificacionFamiliar
        fields = '__all__'

    def get_paciente_nombre(self, obj) -> str:
        return f"{obj.paciente.tipo_cedula}-{obj.paciente.cedula} {obj.paciente.nombre} {obj.paciente.apellido}"


# ==========================================
# 4. CONTROL DE EQUIPOS TECNOLÓGICOS
# ==========================================
class InventarioEquipoSerializer(serializers.ModelSerializer):
    responsable_nombre = serializers.CharField(source='responsable.__str__', read_only=True)

    class Meta:
        model = InventarioEquipo
        fields = '__all__'


# ==========================================
# 5. ESTADÍSTICAS POBLACIONALES Y TERRITORIO
# ==========================================
class SectorCPTSerializer(serializers.ModelSerializer):
    comuna_nombre = serializers.CharField(source='comuna.nombre', read_only=True)

    class Meta:
        model = SectorCPT
        fields = '__all__'


class ComunaSerializer(serializers.ModelSerializer):
    total_poblacion = serializers.ReadOnlyField()
    total_familias = serializers.ReadOnlyField()
    sectores = SectorCPTSerializer(many=True, read_only=True)

    class Meta:
        model = Comuna
        fields = '__all__'


class IndicadorPoblacionalASICSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndicadorPoblacionalASIC
        fields = '__all__'


# ==========================================
# 6. SINCRONIZACIÓN DIFERIDA (OFFLINE-FIRST)
# ==========================================
class SyncBatchRequestSerializer(serializers.Serializer):
    """Payload para sincronización por lotes (Offline-First /api/v1/sync/batch/)"""
    pacientes = PacienteSerializer(many=True, required=False, default=list)
    turnos = TurnoSerializer(many=True, required=False, default=list)
    controles_endocrinos = ControlEndocrinoSerializer(many=True, required=False, default=list)
    controles_respiratorios = ControlRespiratorioSerializer(many=True, required=False, default=list)
    rutas_maternas = RutaMaternaSerializer(many=True, required=False, default=list)
    planificacion_familiar = PlanificacionFamiliarSerializer(many=True, required=False, default=list)

