from django.shortcuts import render
from .models import Tarea


def lista_tareas(request):
    tareas = Tarea.objects.all()
    contexto = {'tareas': tareas}
    return render(request, 'tareas/lista_tareas.html', contexto)

