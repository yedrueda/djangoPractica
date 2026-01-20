from django import forms
from django.contrib.auth.models import User, Group
from .models import Paciente, Consulta

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'cedula': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = [
            'programa', 'motivo', 'diagnostico', 'tratamiento', 
            'tension_arterial', 'peso_madre', 'fur', 'glicemia'
        ]
        widgets = {
            'programa': forms.Select(attrs={'class': 'form-select'}),
            'tension_arterial': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ejemplo: 120/80' # <--- AQUÍ ES EL LUGAR CORRECTO
            }),
            'fur': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'peso_madre': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Peso en kg'}),
            'glicemia': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Glicemia mg/dL'}),
            'motivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'diagnostico': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'tratamiento': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class EditarUsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active']
        # Si quieres evitar que cambien el username, puedes hacerlo así:
        widgets = {
            'username': forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

        rol = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=False,
        label="Rol en el CDI",
        widget=forms.Select(attrs={'class': 'form-select'}) # <-- Verifica que cierre aquí
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


  