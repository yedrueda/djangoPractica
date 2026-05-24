from django import forms
from .models import Paciente, PersonalCDI, InventarioEquipo, ControlEndocrino, RutaMaterna, PlanificacionFamiliar

from django import forms
from .models import Paciente

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
        exclude = ['usuario_id']
        widgets = {
            'tipo_cedula': forms.Select(attrs={'class': 'form-select', 'style': 'width: 80px; border-top-right-radius: 0; border-bottom-right-radius: 0;'}),
            'cedula': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 12345678', 'style': 'border-top-left-radius: 0; border-bottom-left-radius: 0;'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'rol_profesional': forms.Select(attrs={'class': 'form-select'}),
            'especialidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Medicina General'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'estatus': forms.Select(attrs={'class': 'form-select'}),
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
        super(ControlEndocrinoForm, self).__init__(*args, **kwargs)
        # Formato del buscador de paciente
        self.fields['paciente'].label_from_instance = lambda obj: f"{obj.tipo_cedula}-{obj.cedula} | {obj.nombre} {obj.apellido}"

    class Meta:
        model = ControlEndocrino
        fields = [
            'paciente', 'sede_tratamiento', 'pas', 'tension_arterial', 'frecuencia_cardiaca', 
            'frecuencia_respiratoria', 'temperatura', 'peso_kg', 'talla_cm', 'glucemia_ayunas', 
            'hba1c', 'creatinina', 'urea', 'tgo', 'tgp', 'colesterol_total', 'trigliceridos',
            'asociacion_cv', 'insulina', 'enfermedad_renal_cronica', 'obesidad', 
            'diabetes_mellitus', 'enf_tiroidea', 'sobre_peso', 'pie_diabetico', 
            'dislipidemia', 'medicamentos_entregados', 'referencia', 'conducta', 
            'diagnostico', 'tratamiento', 'otras_patologias', 'alergias', 'observaciones_finales'
        ]
        
        labels = {
            'paciente': 'Paciente',
            'sede_tratamiento': 'Sede de Tratamiento',
            'pas': 'Tipo de Consulta (P.A.S)',
            'tension_arterial': 'Tensión Arterial (mmHg)',
            'frecuencia_cardiaca': 'Frecuencia Cardíaca (lpm)',
            'frecuencia_respiratoria': 'Frecuencia Respiratoria (rpm)',
            'temperatura': 'Temperatura (°C)',
            'peso_kg': 'Peso (Kg)',
            'talla_cm': 'Talla (cm)',
            'glucemia_ayunas': 'Glicemia Ayunas (mg/dL)',
            'hba1c': 'HbA1c (%)',
            'creatinina': 'Creatinina (mg/dL)',
            'urea': 'Urea (mg/dL)',
            'tgo': 'TGO (U/L)',
            'tgp': 'TGP (U/L)',
            'colesterol_total': 'Colesterol Total (mg/dL)',
            'trigliceridos': 'Triglicéridos (mg/dL)',
            'medicamentos_entregados': 'Medicamentos Entregados',
            'referencia': 'Referencia',
            'conducta': 'Conducta Médica',
            'diagnostico': 'Diagnóstico',
            'tratamiento': 'Tratamiento e Indicaciones',
            'otras_patologias': 'Otras Patologías',
            'alergias': 'Alergias',
            'observaciones_finales': 'Observaciones Finales'
        }
        
        widgets = {
            # Selección y Texto
            'paciente': forms.Select(attrs={'class': 'form-select'}),
            'sede_tratamiento': forms.TextInput(attrs={'class': 'form-control'}),
            'pas': forms.Select(attrs={'class': 'form-select'}),
            
            # Signos Vitales y Labs
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
            
            # Textareas
            'medicamentos_entregados': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'referencia': forms.TextInput(attrs={'class': 'form-control'}),
            'conducta': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'diagnostico': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'tratamiento': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'otras_patologias': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'alergias': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'observaciones_finales': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            
            # Checkboxes (Patologías)
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