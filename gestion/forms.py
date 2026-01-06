from django import forms
from .models import Paciente, Consulta

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['cedula', 'nombres', 'apellidos', 'fecha_nacimiento', 'telefono', 'direccion']
        # Esto es un toque pro: agregamos widgets para que la fecha tenga un calendario
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'cedula': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: V-12345678'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['motivo', 'sintomas', 'presion_arterial', 'temperatura', 'diagnostico', 'tratamiento']
        
        widgets = {
            'motivo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Fiebre alta y dolor de cabeza'}),
            'sintomas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'diagnostico': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tratamiento': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'presion_arterial': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 120/80'}),
            'temperatura': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 37.5'}),
        }