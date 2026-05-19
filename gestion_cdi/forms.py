from django import forms
from .models import Paciente, PersonalCDI, InventarioEquipo, ControlEndocrino

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'
        widgets = {
            'tipo_cedula': forms.Select(attrs={'class': 'form-select', 'style': 'width: 80px; border-top-right-radius: 0; border-bottom-right-radius: 0;'}),
            'cedula': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 12345678', 'style': 'border-top-left-radius: 0; border-bottom-left-radius: 0;'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'sexo': forms.Select(attrs={'class': 'form-select'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'asic': forms.TextInput(attrs={'class': 'form-control'}),
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
    class Meta:
        model = ControlEndocrino
        fields = '__all__'
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-select'}),
            'medico_tratante': forms.Select(attrs={'class': 'form-select'}),
            'tension_arterial': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 120/80'}),
            'frecuencia_cardiaca': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'LPM'}),
            'frecuencia_respiratoria': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'RPM'}),
            'temperatura': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': '°C'}),
            'peso_kg': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Kg'}),
            'talla_cm': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'cm'}),
            'glucemia_ayunas': forms.NumberInput(attrs={'class': 'form-control'}),
            'diagnostico': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tratamiento': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }