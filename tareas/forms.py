from django import forms
from .models import Tarea

class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion'] 
        # No incluimos 'completada' porque al crearla, por defecto está pendiente.
       