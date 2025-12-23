from django.shortcuts import redirect, render
from .models import Tarea
from .forms import TareaForm

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