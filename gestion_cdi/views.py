from django.shortcuts import render
from .models import Paciente, PersonalCDI, InventarioEquipo

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
