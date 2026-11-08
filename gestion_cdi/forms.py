from django import forms
from .models import (
    Paciente, PersonalCDI, InventarioEquipo, ControlEndocrino, ControlRespiratorio,
    RutaMaterna, PlanificacionFamiliar, TurnoGuardia, 
    Comuna, SectorCPT, IndicadorPoblacionalASIC
)

class PacienteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Campos con valor por defecto en el modelo no deben bloquear envíos parciales
        campos_con_default = [
            'estado_civil', 'asic', 'municipio', 'parroquia',
            'grupo_sanguineo', 'alergias', 'carnet_de_la_patria',
            'posee_discapacidad', 'gestante',
        ]
        for campo in campos_con_default:
            if campo in self.fields:
                self.fields[campo].required = False

    class Meta:
        model = Paciente
        fields = [
            # 1. Identificación y Sociodemográficos
            'tipo_cedula', 'cedula', 'nombre', 'apellido', 'fecha_nacimiento',
            'sexo', 'estado_civil', 'ocupacion', 'telefono', 'correo', 'carnet_de_la_patria',
            # 2. Ubicación Territorial (ASIC El Llanito)
            'asic', 'municipio', 'parroquia', 'comuna', 'sector_cpt', 'direccion',
            # 3. Contacto de Emergencia
            'contacto_emergencia_nombre', 'contacto_emergencia_parentesco', 'contacto_emergencia_telefono',
            # 4. Perfil Clínico Base y Alertas
            'grupo_sanguineo', 'alergias', 'antecedentes_personales', 'antecedentes_familiares',
            'posee_discapacidad', 'detalle_discapacidad', 'gestante',
        ]
        labels = {
            'tipo_cedula': 'Nac.',
            'cedula': 'Cédula de Identidad',
            'nombre': 'Nombres',
            'apellido': 'Apellidos',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'sexo': 'Sexo',
            'estado_civil': 'Estado Civil',
            'ocupacion': 'Ocupación u Oficio',
            'telefono': 'Teléfono de Contacto',
            'correo': 'Correo Electrónico',
            'carnet_de_la_patria': 'Posee Carnet de la Patria',
            'asic': 'ASIC',
            'municipio': 'Municipio',
            'parroquia': 'Parroquia',
            'comuna': 'Comuna de Adscripción',
            'sector_cpt': 'Consultorio Popular (CPT) / Sector',
            'direccion': 'Dirección de Habitación / Punto de Referencia',
            'contacto_emergencia_nombre': 'Familiar / Contacto de Emergencia',
            'contacto_emergencia_parentesco': 'Parentesco',
            'contacto_emergencia_telefono': 'Teléfono de Emergencia',
            'grupo_sanguineo': 'Grupo Sanguíneo y Rh',
            'alergias': 'Alergias Medicamentosas / Alimentarias',
            'antecedentes_personales': 'Antecedentes Patológicos Personales',
            'antecedentes_familiares': 'Antecedentes Familiares',
            'posee_discapacidad': 'Posee Discapacidad',
            'detalle_discapacidad': 'Tipo / Detalle de Discapacidad',
            'gestante': 'Paciente Gestante (Embarazada)',
        }
        widgets = {
            'tipo_cedula': forms.Select(
                choices=[('V', 'V'), ('E', 'E'), ('P', 'P'), ('M', 'M')],
                attrs={'class': 'form-select', 'style': 'width: 85px; border-top-right-radius: 0; border-bottom-right-radius: 0;'}
            ),
            'cedula': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 14852963', 'style': 'border-top-left-radius: 0; border-bottom-left-radius: 0;'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: María Fernanda'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Rojas Pérez'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'id_fecha_nacimiento'}),
            'sexo': forms.Select(attrs={'class': 'form-select'}),
            'estado_civil': forms.Select(attrs={'class': 'form-select'}),
            'ocupacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Docente, Comerciante, Estudiante...'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 0412-5558912'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@correo.com'}),
            'carnet_de_la_patria': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
            'asic': forms.TextInput(attrs={'class': 'form-control'}),
            'municipio': forms.TextInput(attrs={'class': 'form-control'}),
            'parroquia': forms.TextInput(attrs={'class': 'form-control'}),
            'comuna': forms.Select(attrs={'class': 'form-select'}),
            'sector_cpt': forms.Select(attrs={'class': 'form-select'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Av., Calle, Vereda, N° de Casa y Punto de Referencia'}),
            'contacto_emergencia_nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre y Apellido del familiar'}),
            'contacto_emergencia_parentesco': forms.Select(attrs={'class': 'form-select'}),
            'contacto_emergencia_telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 0414-3216549'}),
            'grupo_sanguineo': forms.Select(attrs={'class': 'form-select'}),
            'alergias': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Ej: Penicilina, AINES, Mariscos o Ninguna conocida'}),
            'antecedentes_personales': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Ej: HTA, Diabetes Tipo 2, Asma Bronquial, Cirugías previas...'}),
            'antecedentes_familiares': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Ej: Madre diabética, Padre hipertenso...'}),
            'posee_discapacidad': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
            'detalle_discapacidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Motora, Visual, Auditiva...'}),
            'gestante': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
        }

class PersonalCDIForm(forms.ModelForm):
    class Meta:
        model = PersonalCDI
        exclude = ['usuario']
        widgets = {
            'tipo_cedula': forms.Select(attrs={'class': 'form-select', 'style': 'width: 80px; border-top-right-radius: 0; border-bottom-right-radius: 0;'}),
            'cedula': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 12345678', 'style': 'border-top-left-radius: 0; border-bottom-left-radius: 0;'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'rol_profesional': forms.Select(attrs={'class': 'form-select'}),
            'especialidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Medicina General'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'estatus': forms.Select(attrs={'class': 'form-select'}),
            'carnet_de_la_patria': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
            'fecha_ingreso': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class InventarioEquipoForm(forms.ModelForm):
    class Meta:
        model = InventarioEquipo
        fields = '__all__'
        widgets = {
            'codigo_bien_nacional': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: BN-12345'}),
            'nombre_equipo': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_equipo': forms.Select(attrs={'class': 'form-select'}),
            'ubicacion_especifica': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Consultorio 2'}),
            'estado_fisico': forms.Select(attrs={'class': 'form-select'}),
            'responsable_mantenimiento': forms.Select(attrs={'class': 'form-select'}),
            'ultima_revision': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'proximo_mantenimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class ControlEndocrinoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['paciente'].label_from_instance = lambda obj: f"{obj.tipo_cedula}-{obj.cedula} | {obj.nombre} {obj.apellido}"
        # Optimización para alto volumen de pacientes: en GET solo precarga los 50 más recientes
        # (el resto se busca dinámicamente vía /api/v1/pacientes/autocompletar/)
        if not self.is_bound:
            recientes_ids = list(Paciente.objects.order_by('-fecha_registro').values_list('cedula', flat=True)[:50])
            paciente_inicial = self.initial.get('paciente') or getattr(self.instance, 'paciente_id', None)
            if paciente_inicial and int(paciente_inicial) not in recientes_ids:
                recientes_ids.append(int(paciente_inicial))
            self.fields['paciente'].queryset = Paciente.objects.filter(cedula__in=recientes_ids)

        for campo in ['tipo_diabetes', 'clasificacion_pie_diabetico', 'riesgo_cardiovascular', 'tiras_reactivas_entregadas']:
            if campo in self.fields:
                self.fields[campo].required = False

    class Meta:
        model = ControlEndocrino
        exclude = ['fecha_atencion']
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-select'}),
            'atendido_por': forms.Select(attrs={'class': 'form-select'}),
            'sede_tratamiento': forms.TextInput(attrs={'class': 'form-control'}),
            'pas': forms.Select(attrs={'class': 'form-select'}),
            'semana_epidemiologica': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 53, 'placeholder': 'Ej: 44'}),
            'tension_arterial': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 130/85'}),
            'frecuencia_cardiaca': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 78'}),
            'frecuencia_respiratoria': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 18'}),
            'temperatura': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'Ej: 36.6'}),
            'peso_kg': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'id': 'id_peso_kg', 'placeholder': 'Ej: 84.5'}),
            'talla_cm': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_talla_cm', 'placeholder': 'Ej: 165'}),
            'circunferencia_abdominal_cm': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'Ej: 98.0'}),
            'glucemia_ayunas': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'mg/dL'}),
            'glucemia_postprandial': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'mg/dL (2h)'}),
            'hba1c': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'Ej: 7.8'}),
            'creatinina': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'mg/dL'}),
            'urea': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'mg/dL'}),
            'acido_urico': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'mg/dL'}),
            'proteinuria_24h': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'mg/24h'}),
            'tgo': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'U/L'}),
            'tgp': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'U/L'}),
            'colesterol_total': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'mg/dL'}),
            'colesterol_hdl': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'mg/dL'}),
            'colesterol_ldl': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'mg/dL'}),
            'trigliceridos': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'mg/dL'}),
            'tsh': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'µUI/mL'}),
            't4_libre': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'ng/dL'}),
            'tipo_diabetes': forms.Select(attrs={'class': 'form-select'}),
            'clasificacion_pie_diabetico': forms.Select(attrs={'class': 'form-select'}),
            'riesgo_cardiovascular': forms.Select(attrs={'class': 'form-select'}),
            'esquema_insulina': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Insulina NPH 20 UI SC 7:00 AM y 10 UI SC 9:00 PM'}),
            'tiras_reactivas_entregadas': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'medicamentos_entregados': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Ej: Metformina 850mg #60, Losartán Potásico 50mg #30, Atorvastatina 20mg #30'}),
            'diagnostico': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Ej: 1. Diabetes Mellitus Tipo 2 descompensada. 2. HTA Estadio 1. 3. Dislipidemia mixta.'}),
            'tratamiento': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Ej: Metformina 850mg VO c/12h con comidas, Losartán 50mg VO OD, dieta hipoglúcida e hiposódica.'}),
            'conducta': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Educación diabetológica, cuidado preventivo de los pies, control de glucemia capilar.'}),
            'otras_patologias': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'alergias': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'observaciones_finales': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'referencia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Oftalmología (Fondo de ojo) / Nefrología / Nutrición'}),
            'proxima_cita': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            # Checkboxes puros (Control Operativo Regional CAREMT)
            'asociacion_cv': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hipertension_arterial': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'insulina': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'enfermedad_renal_cronica': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'obesidad': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'diabetes_mellitus': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'enf_tiroidea': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sobre_peso': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pie_diabetico': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'dislipidemia': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ControlRespiratorioForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['paciente'].label_from_instance = lambda obj: f"{obj.tipo_cedula}-{obj.cedula} | {obj.nombre} {obj.apellido}"
        if not self.is_bound:
            recientes_ids = list(Paciente.objects.order_by('-fecha_registro').values_list('cedula', flat=True)[:50])
            paciente_inicial = self.initial.get('paciente') or getattr(self.instance, 'paciente_id', None)
            if paciente_inicial and int(paciente_inicial) not in recientes_ids:
                recientes_ids.append(int(paciente_inicial))
            self.fields['paciente'].queryset = Paciente.objects.filter(cedula__in=recientes_ids)
        for campo in ['severidad_cuadro', 'resultado_bk', 'sede_tratamiento', 'pas']:
            if campo in self.fields:
                self.fields[campo].required = False

    class Meta:
        model = ControlRespiratorio
        exclude = ['fecha_atencion']
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-select'}),
            'atendido_por': forms.Select(attrs={'class': 'form-select'}),
            'sede_tratamiento': forms.TextInput(attrs={'class': 'form-control'}),
            'pas': forms.Select(attrs={'class': 'form-select'}),
            'semana_epidemiologica': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 53, 'placeholder': 'Ej: 45'}),
            'saturacion_oxigeno': forms.NumberInput(attrs={'class': 'form-control', 'min': 40, 'max': 100, 'id': 'id_saturacion_oxigeno', 'placeholder': 'Ej: 96'}),
            'frecuencia_respiratoria': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 20'}),
            'frecuencia_cardiaca': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 84'}),
            'temperatura': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'Ej: 37.2'}),
            'tension_arterial': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 120/80'}),
            'flujo_espiratorio_pico': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'L/min (PEF)'}),
            'severidad_cuadro': forms.Select(attrs={'class': 'form-select'}),
            'esquema_nebulizacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Salbutamol 15 gotas + Bromuro de Ipratropio 10 gotas en 3cc Sol. 0.9% (3 ciclos)'}),
            'litros_oxigeno_min': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5', 'placeholder': 'Ej: 3.0 L/min'}),
            'resultado_bk': forms.Select(attrs={'class': 'form-select'}),
            'hallazgos_radiografia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Atrapamiento aéreo bilateral, sin infiltrados neumónicos'}),
            'diagnostico': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Ej: Crisis aguda de Asma Bronquial moderada / Infección Respiratoria Aguda'}),
            'tratamiento': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Ej: Salbutamol inhalador 2 puff c/6h por 7 días, Prednisona 50mg VO OD por 5 días'}),
            'medicamentos_entregados': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Ej: Salbutamol 100mcg IDM (1 unid), Loratadina 10mg (#10 tab)'}),
            'referencia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Consulta de Neumología / Tisiología'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Evolución tras terapia respiratoria en sala y recomendaciones'}),
            'proxima_cita': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            # Checkboxes
            'asma_bronquial': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'epoc': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'infeccion_respiratoria_aguda': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'neumonia': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sospecha_tuberculosis': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'rinitis_alergica': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tabaquismo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tos_con_expectoracion': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'disnea': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sibilancias': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'nebulizacion_realizada': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'oxigenoterapia': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'baciloscopia_solicitada': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class RutaMaternaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RutaMaternaForm, self).__init__(*args, **kwargs)
        self.fields['paciente'].label_from_instance = lambda obj: f"{obj.tipo_cedula}-{obj.cedula} | {obj.nombre} {obj.apellido}"
        if not self.is_bound:
            recientes_ids = list(Paciente.objects.order_by('-fecha_registro').values_list('cedula', flat=True)[:50])
            paciente_inicial = self.initial.get('paciente') or getattr(self.instance, 'paciente_id', None)
            if paciente_inicial and int(paciente_inicial) not in recientes_ids:
                recientes_ids.append(int(paciente_inicial))
            self.fields['paciente'].queryset = Paciente.objects.filter(cedula__in=recientes_ids)
        for campo in [
            'pas', 'numero_control_prenatal', 'gestas', 'paras', 'cesareas', 'abortos',
            'movimientos_fetales', 'presentacion_fetal', 'vdrl_estatus', 'vih_estatus',
            'riesgo_obstetrico', 'centro_parto_programado'
        ]:
            if campo in self.fields:
                self.fields[campo].required = False

    class Meta:
        model = RutaMaterna
        exclude = ['fecha_control']
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-select'}),
            'atendido_por': forms.Select(attrs={'class': 'form-select'}),
            'pas': forms.Select(attrs={'class': 'form-select'}),
            'numero_control_prenatal': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'eje': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Comuna 1 - CPT El Llanito'}),
            'direccion_detallada': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'fum': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'id_fum'}),
            'fpp': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'id_fpp'}),
            'semanas_embarazo': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 43, 'id': 'id_semanas_embarazo', 'placeholder': 'Ej: 24'}),
            'gestas': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'paras': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'cesareas': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'abortos': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'tension_arterial': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 110/70'}),
            'peso_kg': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'Kg'}),
            'talla_cm': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'cm'}),
            'altura_uterina_cm': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5', 'placeholder': 'cm'}),
            'frecuencia_cardiaca_fetal': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '120 - 160 lpm'}),
            'movimientos_fetales': forms.Select(attrs={'class': 'form-select'}),
            'presentacion_fetal': forms.Select(attrs={'class': 'form-select'}),
            'hemoglobina': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'g/dL'}),
            'glucemia_ayunas': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'mg/dL'}),
            'vdrl_estatus': forms.Select(attrs={'class': 'form-select'}),
            'vih_estatus': forms.Select(attrs={'class': 'form-select'}),
            'riesgo_obstetrico': forms.Select(attrs={'class': 'form-select'}),
            'signos_alarma': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Sangrado genital, cefalea intensa, visión borrosa, pérdida de líquido...'}),
            'centro_parto_programado': forms.TextInput(attrs={'class': 'form-control'}),
            'diagnostico': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Ej: Embarazo simple de 24 semanas por FUM, Bajo Riesgo Obstétrico (ARO I)'}),
            'tratamiento': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Ej: Sulfato Ferroso 300mg OD, Ácido Fólico 5mg OD, Calcio 600mg OD'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'proxima_cita': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            # Checkboxes
            'edema_miembros_inferiores': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'infeccion_urinaria': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'toxoide_tetanico': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'acido_folico_entregado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sulfato_ferroso_entregado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'polivitaminicos_entregados': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class PlanificacionFamiliarForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PlanificacionFamiliarForm, self).__init__(*args, **kwargs)
        self.fields['paciente'].label_from_instance = lambda obj: f"{obj.tipo_cedula}-{obj.cedula} | {obj.nombre} {obj.apellido}"
        if not self.is_bound:
            recientes_ids = list(Paciente.objects.order_by('-fecha_registro').values_list('cedula', flat=True)[:50])
            paciente_inicial = self.initial.get('paciente') or getattr(self.instance, 'paciente_id', None)
            if paciente_inicial and int(paciente_inicial) not in recientes_ids:
                recientes_ids.append(int(paciente_inicial))
            self.fields['paciente'].queryset = Paciente.objects.filter(cedula__in=recientes_ids)
        for campo in [
            'primera_sucesiva', 'establecimiento_salud', 'municipio', 'prueba_embarazo',
            'tipo_metodo', 'preservativo_masculino', 'preservativo_femenino',
            'blister_orales_entregados', 'ampollas_inyectables', 'diu', 'implante'
        ]:
            if campo in self.fields:
                self.fields[campo].required = False

    class Meta:
        model = PlanificacionFamiliar
        exclude = ['fecha_atencion']
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-select'}),
            'atendido_por': forms.Select(attrs={'class': 'form-select'}),
            'semana': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 53, 'placeholder': 'Ej: 45'}),
            'primera_sucesiva': forms.Select(attrs={'class': 'form-select'}),
            'establecimiento_salud': forms.TextInput(attrs={'class': 'form-control'}),
            'municipio': forms.TextInput(attrs={'class': 'form-control'}),
            'tension_arterial': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 115/75'}),
            'peso_kg': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'Kg'}),
            'fum': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'prueba_embarazo': forms.Select(attrs={'class': 'form-select'}),
            'tipo_metodo': forms.Select(attrs={'class': 'form-select'}),
            'metodo_entregado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Levonorgestrel/Etinilestradiol 0.15/0.03mg'}),
            'preservativo_masculino': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'preservativo_femenino': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'blister_orales_entregados': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'ampollas_inyectables': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'diu': forms.Select(attrs={'class': 'form-select'}),
            'implante': forms.Select(attrs={'class': 'form-select'}),
            'antecedente_obstetrico': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Menarquia, ciclos menstruales, gestas/paras previas, métodos usados...'}),
            'diagnostico': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Ej: Usuaria sana apta para anticoncepción hormonal combinada (Categoría 1 OMS)'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'proxima_cita': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            # Checkboxes
            'consejeria_salud_sexual': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'prevencion_its_vih': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'citologia_realizada': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'autoexamen_mamario': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'despistaje_its_solicitado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class TurnoGuardiaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['personal'].label_from_instance = lambda obj: f"{obj.tipo_cedula}-{obj.cedula} | {obj.nombre} {obj.apellido} ({obj.rol_profesional})"
        self.fields['suplente'].label_from_instance = lambda obj: f"{obj.tipo_cedula}-{obj.cedula} | {obj.nombre} {obj.apellido} ({obj.rol_profesional})"
        self.fields['suplente'].required = False

    class Meta:
        model = TurnoGuardia
        fields = ['personal', 'fecha', 'tipo_turno', 'area_servicio', 'estado', 'suplente', 'observaciones']
        labels = {
            'personal': 'Personal Titular',
            'fecha': 'Fecha de la Guardia',
            'tipo_turno': 'Tipo de Turno / Horario',
            'area_servicio': 'Área o Servicio Asignado',
            'estado': 'Estatus de la Guardia',
            'suplente': 'Personal Suplente (Opcional)',
            'observaciones': 'Novedades / Observaciones',
        }
        widgets = {
            'personal': forms.Select(attrs={'class': 'form-select'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tipo_turno': forms.Select(attrs={'class': 'form-select'}),
            'area_servicio': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'suplente': forms.Select(attrs={'class': 'form-select'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Detalles de la guardia, sustitución o novedades...'}),
        }

class SectorCPTForm(forms.ModelForm):
    class Meta:
        model = SectorCPT
        fields = ['comuna', 'numero', 'nombre', 'tipo_cpt', 'poblacion', 'familias', 'medico_responsable', 'situacion_espacio', 'observaciones']
        labels = {
            'comuna': 'Comuna a la que Pertenece',
            'numero': 'Número de CPT / Sector',
            'nombre': 'Nombre del Consultorio Popular / Sector',
            'tipo_cpt': 'Tipo de CPT',
            'poblacion': 'Población Estimada (Habitantes)',
            'familias': 'Número de Familias Censadas',
            'medico_responsable': 'Médicos Asignados',
            'situacion_espacio': 'Estado del Espacio Físico',
            'observaciones': 'Novedades / Observaciones',
        }
        widgets = {
            'comuna': forms.Select(attrs={'class': 'form-select'}),
            'numero': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: La Cooperativa'}),
            'tipo_cpt': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: CPT 1-2 o CPT 3'}),
            'poblacion': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'familias': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'medico_responsable': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Dra. Ruth Hdz (Artic. 8)'}),
            'situacion_espacio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Operativo, Sin Espacio Físico, Colegio, En Reparación...'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Detalles sobre la infraestructura o territorio...'}),
        }

class IndicadorPoblacionalForm(forms.ModelForm):
    class Meta:
        model = IndicadorPoblacionalASIC
        fields = ['poblacion_total', 'familias_total', 'comunas_total', 'femenino_total', 'masculino_total', 'red_referencia']
        widgets = {
            'poblacion_total': forms.NumberInput(attrs={'class': 'form-control'}),
            'familias_total': forms.NumberInput(attrs={'class': 'form-control'}),
            'comunas_total': forms.NumberInput(attrs={'class': 'form-control'}),
            'femenino_total': forms.NumberInput(attrs={'class': 'form-control'}),
            'masculino_total': forms.NumberInput(attrs={'class': 'form-control'}),
            'red_referencia': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }