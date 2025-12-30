from django.shortcuts import redirect, render
from .models import Tarea
from .forms import TareaForm
from django.shortcuts import render, redirect, get_object_or_404

def lista_tareas(request):
    tareas = Tarea.objects.all()
    contexto = {'tareas': tareas}
    return render(request, 'tareas/lista_tareas.html', contexto)

def crear_tarea(request):
    if request.method == 'POST':
        # si el usuario envio datos , los cargamos al formulario 
        form = TareaForm(request.POST)
        if form.is_valid():
            form.save() # Guardar en la base de datos 
            return redirect('lista_tareas')
            
    else:
        # Si el usuario solo entró a la página, formulario vacío
        form = TareaForm()
    
    return render(request, 'tareas/crear_tarea.html', {'form': form})

def eliminar_tarea(request, tarea_id):
    #busca las tareas por id, si no existe devuelve error 404
    tarea = get_object_or_404(Tarea, id=tarea_id)
    tarea.delete()
    return redirect('lista_tareas')

def completar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)
    tarea.completada = True # cambiamos el estado de la tarea
    tarea.save() # guardamos los cambios en la base de datos
    return redirect('lista_tareas')

