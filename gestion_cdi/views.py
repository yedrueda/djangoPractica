from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Paciente, PersonalCDI, InventarioEquipo, ControlEndocrino
from .forms import PacienteForm, PersonalCDIForm, InventarioEquipoForm, ControlEndocrinoForm





@login_required
def inicio(request):
    total_pacientes = Paciente.objects.count()
    total_personal = PersonalCDI.objects.count()
    total_equipos = InventarioEquipo.objects.count()
    total_consultas = ControlEndocrino.objects.count() # <-- NUEVA LÍNEA: Contamos las consultas

    contexto = {
        'total_pacientes': total_pacientes,
        'total_personal': total_personal,
        'total_equipos': total_equipos,
        'total_consultas': total_consultas, # <-- NUEVA LÍNEA: Lo pasamos al HTML
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

# ==========================================
# CRUD DE PERSONAL DEL CDI
# ==========================================

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

# ==========================================
# CRUD DE INVENTARIO DE EQUIPOS
# ==========================================

@login_required
def lista_equipos(request):
    equipos = InventarioEquipo.objects.all()
    return render(request, 'gestion_cdi/lista_equipos.html', {'equipos': equipos})

@login_required
def crear_equipo(request):
    if request.method == 'POST':
        form = InventarioEquipoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_equipos')
    else:
        form = InventarioEquipoForm()
    return render(request, 'gestion_cdi/crear_equipo.html', {'form': form})

@login_required
def editar_equipo(request, id):
    equipo = get_object_or_404(InventarioEquipo, id=id)
    if request.method == 'POST':
        form = InventarioEquipoForm(request.POST, instance=equipo)
        if form.is_valid():
            form.save()
            return redirect('lista_equipos')
    else:
        form = InventarioEquipoForm(instance=equipo)
    return render(request, 'gestion_cdi/editar_equipo.html', {'form': form, 'equipo': equipo})

@login_required
def borrar_equipo(request, id):
    equipo = get_object_or_404(InventarioEquipo, id=id)
    if request.method == 'POST':
        equipo.delete()
        return redirect('lista_equipos')
    return render(request, 'gestion_cdi/borrar_equipo.html', {'equipo': equipo})

# ==========================================
# MÓDULO CLÍNICO: CONSULTAS Y SIGNOS VITALES
# ==========================================

@login_required
def lista_consultas(request):
    controles = ControlEndocrino.objects.all().order_by('-fecha_atencion')
    return render(request, 'gestion_cdi/lista_consultas.html', {'controles': controles})

@login_required
def crear_consulta(request):
    if request.method == 'POST':
        form = ControlEndocrinoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_consultas')
    else:
        form = ControlEndocrinoForm()
    return render(request, 'gestion_cdi/crear_consulta.html', {'form': form})

@login_required
def editar_consulta(request, id):
    consulta = get_object_or_404(ControlEndocrino, id=id)
    if request.method == 'POST':
        form = ControlEndocrinoForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            return redirect('lista_consultas')
    else:
        form = ControlEndocrinoForm(instance=consulta)
    return render(request, 'gestion_cdi/editar_consulta.html', {'form': form, 'consulta': consulta})

@login_required
def borrar_consulta(request, id):
    consulta = get_object_or_404(ControlEndocrino, id=id)
    if request.method == 'POST':
        consulta.delete()
        return redirect('lista_consultas')
    return render(request, 'gestion_cdi/borrar_consulta.html', {'consulta': consulta})