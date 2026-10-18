from django import forms
from .models import (
    Paciente, PersonalCDI, InventarioEquipo, ControlEndocrino, 
    RutaMaterna, PlanificacionFamiliar, TurnoGuardia, 
    Comuna, SectorCPT, IndicadorPoblacionalASIC
)

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        # 1. Se incluye 'tipo_cedula' en la lista de campos obligatorios
        fields = ['tipo_cedula', 'cedula', 'nombre', 'apellido', 'fecha_nacimiento', 'sexo', 'direccion', 'telefono']
        
        # 2. Se añade la etiqueta para el nuevo campo
        labels = {
            'tipo_cedula': 'Nac.',
            'cedula': 'Cédula de Identidad',
            'nombre': 'Nombres',
            'apellido': 'Apellidos',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'sexo': 'Sexo',
            'direccion': 'Dirección de Habitación',
            'telefono': 'Teléfono de Contacto',
        }
        
        # 3. Diccionario de widgets limpio y sin duplicados
        widgets = {
            'tipo_cedula': forms.Select(
                choices=[('V', 'V'), ('E', 'E')], 
                attrs={'class': 'form-select', 'style': 'width: 85px; border-top-right-radius: 0; border-bottom-right-radius: 0;'}
            ),
            'cedula': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 12345678', 'style': 'border-top-left-radius: 0; border-bottom-left-radius: 0;'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'id_fecha_nacimiento'}),
            'sexo': forms.Select(attrs={'class': 'form-select'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
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
    class Meta:
        model = ControlEndocrino
        exclude = ['fecha_atencion']
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-select'}),
            'sede_tratamiento': forms.TextInput(attrs={'class': 'form-control'}),
            'pas': forms.Select(attrs={'class': 'form-select'}),
            'tension_arterial': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 120/80'}),
            'frecuencia_cardiaca': forms.NumberInput(attrs={'class': 'form-control'}),
            'frecuencia_respiratoria': forms.NumberInput(attrs={'class': 'form-control'}),
            'temperatura': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'peso_kg': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'talla_cm': forms.NumberInput(attrs={'class': 'form-control'}),
            'glucemia_ayunas': forms.NumberInput(attrs={'class': 'form-control'}),
            'hba1c': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'creatinina': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'urea': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'tgo': forms.NumberInput(attrs={'class': 'form-control'}),
            'tgp': forms.NumberInput(attrs={'class': 'form-control'}),
            'colesterol_total': forms.NumberInput(attrs={'class': 'form-control'}),
            'trigliceridos': forms.NumberInput(attrs={'class': 'form-control'}),
            'medicamentos_entregados': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'diagnostico': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'tratamiento': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'conducta': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'otras_patologias': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'alergias': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'observaciones_finales': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'referencia': forms.TextInput(attrs={'class': 'form-control'}),
            # Checkboxes puros
            'asociacion_cv': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'insulina': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'enfermedad_renal_cronica': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'obesidad': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'diabetes_mellitus': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'enf_tiroidea': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sobre_peso': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pie_diabetico': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'dislipidemia': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class RutaMaternaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RutaMaternaForm, self).__init__(*args, **kwargs)
        self.fields['paciente'].label_from_instance = lambda obj: f"{obj.tipo_cedula}-{obj.cedula} | {obj.nombre} {obj.apellido}"

    class Meta:
        model = RutaMaterna
        fields = ['paciente', 'semanas_embarazo', 'eje', 'direccion_detallada', 'observaciones']
        labels = {
            'paciente': 'Seleccione la Paciente Gestante',
            'semanas_embarazo': 'Semanas de Gestación',
            'eje': 'Eje Comunitario / Sector',
            'direccion_detallada': 'Dirección Detallada',
            'observaciones': 'Observaciones Clínicas',
        }
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-select'}),
            'semanas_embarazo': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 12'}),
            'eje': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion_detallada': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class PlanificacionFamiliarForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PlanificacionFamiliarForm, self).__init__(*args, **kwargs)
        self.fields['paciente'].label_from_instance = lambda obj: f"{obj.tipo_cedula}-{obj.cedula} | {obj.nombre} {obj.apellido}"

    class Meta:
        model = PlanificacionFamiliar
        fields = ['paciente', 'semana', 'primera_sucesiva', 'establecimiento_salud', 'municipio', 
                  'antecedente_obstetrico', 'preservativo_masculino', 'metodo_entregado', 'diu', 'implante', 'observaciones']
        labels = {
            'paciente': 'Seleccione el/la Paciente',
            'semana': 'Semana Epidemiológica',
            'primera_sucesiva': 'Tipo de Consulta',
            'establecimiento_salud': 'Establecimiento de Salud Base',
            'municipio': 'Municipio',
            'antecedente_obstetrico': 'Antecedentes Obstétricos relevantes',
            'preservativo_masculino': 'Cantidad de Preservativos Entregados',
            'metodo_entregado': 'Método Anticonceptivo',
            'diu': 'Colocación de DIU',
            'implante': 'Colocación de Implante',
            'observaciones': 'Notas del Caso',
        }
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-select'}),
            'semana': forms.NumberInput(attrs={'class': 'form-control'}),
            'primera_sucesiva': forms.Select(choices=[('Primera', 'Primera Vez'), ('Sucesiva', 'Sucesiva')], attrs={'class': 'form-select'}),
            'establecimiento_salud': forms.TextInput(attrs={'class': 'form-control'}),
            'municipio': forms.TextInput(attrs={'class': 'form-control'}),
            'antecedente_obstetrico': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'preservativo_masculino': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'metodo_entregado': forms.TextInput(attrs={'class': 'form-control'}),
            'diu': forms.Select(choices=[('No', 'No'), ('Colocado', 'Colocado'), ('Control', 'Control')], attrs={'class': 'form-select'}),
            'implante': forms.Select(choices=[('No', 'No'), ('Colocado', 'Colocado'), ('Control', 'Control')], attrs={'class': 'form-select'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
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
        fields = '__all__'
        widgets = {
            'poblacion_total': forms.NumberInput(attrs={'class': 'form-control'}),
            'familias_total': forms.NumberInput(attrs={'class': 'form-control'}),
            'comunas_total': forms.NumberInput(attrs={'class': 'form-control'}),
            'femenino_total': forms.NumberInput(attrs={'class': 'form-control'}),
            'masculino_total': forms.NumberInput(attrs={'class': 'form-control'}),
            'tanque_agua_litros': forms.NumberInput(attrs={'class': 'form-control'}),
            'planta_electrica_gasoil_capacidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'planta_electrica_gasoil_actual': forms.NumberInput(attrs={'class': 'form-control'}),
            'red_referencia': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }