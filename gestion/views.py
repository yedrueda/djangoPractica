from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Paciente
from .forms import PacienteForm

@login_required
def lista_pacientes(request):
    # Traer todos los pacientes de la base de datos
    pacientes = Paciente.objects.all() 
    return render(request, 'gestion/lista_pacientes.html', {'pacientes': pacientes})

@login_required
def crear_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_pacientes')# Al terminar, volvemos a la lista
    else:
        form = PacienteForm()
    return render(request, 'gestion/crear_paciente.html', {'form': form})

@login_required
def dashboard(request):
    #contamos los datos reales 
    total_pacientes = Paciente.objects.count()

    #preparamos los datos para enviarlos a la plantilla
    contexto = {
        'total_pacientes': total_pacientes,
        'total_personal': 42,  # Ejemplo estático
        'total_equipos': 15    # Ejemplo estático
    }
    return render(request, 'gestion/home.html', contexto)