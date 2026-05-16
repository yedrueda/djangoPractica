from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Paciente, PersonalCDI, InventarioEquipo
from .forms import PacienteForm


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
            return render(request, 'gestion_cdi/crear_paciente.html', {'form': PacienteForm(), 'success': True})
    else:
        form = PacienteForm()
    return render(request, 'gestion_cdi/crear_paciente.html', {'form': form})