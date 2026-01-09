from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Paciente
from .forms import PacienteForm, ConsultaForm

def es_admin(user):
    return user.groups.filter(name='Administrador').exists() or user.is_superuser

def es_medico(user):
    return user.groups.filter(name='Médico').exists() or es_admin(user)

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

@login_required
@user_passes_test(es_medico)
def registrar_consulta(request, paciente_id):
    # 1. Buscamos al paciente por su ID(si no existe ,error 404)
    paciente = get_object_or_404(Paciente, id=paciente_id)

    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            # TRUCO PRO: Guardamos el formulario en memoria pero NO en base de datos aún
            consulta = form.save(commit=False) 
            # Asignamos el paciente a la consulta
            consulta.paciente = paciente      
            # Finalmente guardamos en la base de datos
            consulta.save()                   
            return redirect('lista_pacientes') # Volvemos a la lista de pacientes
    else:
        form = ConsultaForm()

    return render(request, 'gestion/registrar_consulta.html', {'form': form, 'paciente': paciente})

@login_required
def historia_clinica(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    #Traemos las consultas del paciente ordenadas por fecha (más recientes primero)
    consultas = paciente.consultas.all().order_by('-fecha')

    return render(request, 'gestion/historia_clinica.html', {'paciente': paciente, 'consultas': consultas})

@login_required
@user_passes_test(es_admin)
def editar_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)

    if request.method == 'POST':
        # instance=paciente es la CLAVE: le dice que no cree uno nuevo, sino que edite este
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            return redirect('lista_pacientes')
    else:
        # Aquí cargamos el formulario con los datos viejos para que los veas
        form = PacienteForm(instance=paciente)

    return render(request, 'gestion/editar_paciente.html', {'form': form, 'paciente': paciente})