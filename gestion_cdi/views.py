from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Paciente, PersonalCDI, InventarioEquipo
from .forms import PacienteForm, PersonalCDIForm


@login_required
def inicio(request):
    # Aquí contamos cuántos registros hay para mostrarlos en la pantalla
    total_pacientes = Paciente.objects.count()
    total_personal = PersonalCDI.objects.count()
    total_equipos = InventarioEquipo.objects.count()

    contexto = {
        'total_pacientes': total_pacientes,
        'total_personal': total_personal,
        'total_equipos': total_equipos,
    }
    
    return render(request, 'gestion_cdi/inicio.html', contexto)

# Vista para listar pacientes
@login_required
def lista_pacientes(request):
    pacientes = Paciente.objects.all().order_by('-fecha_registro')  # Ordenamos por fecha de registro, el más reciente primero
    return render(request, 'gestion_cdi/lista_pacientes.html', {'pacientes': pacientes})

# Vista para agregar un nuevo paciente
@login_required
def crear_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_pacientes')
    else:
        form = PacienteForm()
    return render(request, 'gestion_cdi/crear_paciente.html', {'form': form})


@login_required
def editar_paciente(request, cedula):
    paciente = get_object_or_404(Paciente, cedula=cedula)
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            return redirect('lista_pacientes')
    else:
        form = PacienteForm(instance=paciente)
    return render(request, 'gestion_cdi/editar_paciente.html', {'form': form, 'paciente': paciente})    

@login_required
def borrar_paciente(request, cedula):
    paciente = get_object_or_404(Paciente, cedula=cedula)
    if request.method == 'POST':
        paciente.delete()
        return redirect('lista_pacientes')
    return render(request, 'gestion_cdi/borrar_paciente.html', {'paciente': paciente})        

@login_required
def lista_personal(request):
    personal = PersonalCDI.objects.all().order_by('-fecha_ingreso')  # Ordenamos por fecha de ingreso, el más reciente primero
    return render(request, 'gestion_cdi/lista_personal.html', {'personal': personal})

@login_required
def crear_personal(request):
    if request.method == 'POST':
        form = PersonalCDIForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_personal')
    else:
        form = PersonalCDIForm()
    return render(request, 'gestion_cdi/crear_personal.html', {'form': form})

@login_required
def editar_personal(request, cedula):
    personal = get_object_or_404(PersonalCDI, cedula=cedula)
    if request.method == 'POST':
        form = PersonalCDIForm(request.POST, instance=personal)
        if form.is_valid():
            form.save()
            return redirect('lista_personal')
    else:        
        form = PersonalCDIForm(instance=personal)
    return render(request, 'gestion_cdi/editar_personal.html', {'form': form, 'personal': personal})    
               
@login_required
def borrar_personal(request, cedula):
    personal = get_object_or_404(PersonalCDI, cedula=cedula)
    if request.method == 'POST':
        personal.delete()
        return redirect('lista_personal')
    return render(request, 'gestion_cdi/borrar_personal.html', {'personal': personal})  
