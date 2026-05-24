from django import forms
from .models import Paciente, PersonalCDI, InventarioEquipo, ControlEndocrino

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
        # Forzamos a que el desplegable use únicamente nuestra función __str__
        self.fields['paciente'].label_from_instance = lambda obj: f"{obj.tipo_cedula}-{obj.cedula} | {obj.nombre} {obj.apellido}"
    class Meta:
        model = ControlEndocrino
        fields = ['paciente', 'tension_arterial', 'frecuencia_cardiaca', 'frecuencia_respiratoria', 
                  'temperatura', 'peso_kg', 'talla_cm', 'glucemia_ayunas', 'diagnostico', 'tratamiento']
        labels = {
            'paciente': 'Seleccione el Paciente',
            'tension_arterial': 'Tensión Arterial (mmHg)',
            'frecuencia_cardiaca': 'Frecuencia Cardíaca (lpm)',
            'frecuencia_respiratoria': 'Frecuencia Respiratoria (rpm)',
            'temperatura': 'Temperatura (°C)',
            'peso_kg': 'Peso (Kg)',
            'talla_cm': 'Talla (cm)',
            'glucemia_ayunas': 'Glicemia en Ayunas (mg/dL)', # Mantenemos "Glicemia" para la vista
            'diagnostico': 'Diagnóstico Médico',
            'tratamiento': 'Indicaciones y Tratamiento',
        }
        
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-select'}),
            'tension_arterial': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 120/80'}),
            'frecuencia_cardiaca': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 75'}),
            'frecuencia_respiratoria': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 16'}),
            'temperatura': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'Ej: 37.0'}),
            'peso_kg': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'Ej: 70.5'}),
            'talla_cm': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 175'}),
            'glucemia_ayunas': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 95'}),
            'diagnostico': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tratamiento': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }