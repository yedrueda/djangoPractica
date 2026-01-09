from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Paciente
from .forms import PacienteForm, ConsultaForm
from django.contrib.auth.models import User, Group


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


@login_required
@user_passes_test(es_admin)
def lista_usuarios(request):
    usuarios = User.objects.all().prefetch_related('groups')
    return render(request, 'gestion/usuarios_lista.html', {'usuarios': usuarios})

@login_required
@user_passes_test(es_admin)
def crear_usuario(request):
    grupos = Group.objects.all()
    if request.method == 'POST':
        # Capturamos datos del formulario manual
        unombre = request.POST.get('username')
        uclave = request.POST.get('password')
        ugrupo = request.POST.get('grupo')
        
        # Crear el usuario
        nuevo_u = User.objects.create_user(username=unombre, password=uclave)
        nuevo_u.first_name = request.POST.get('first_name')
        nuevo_u.last_name = request.POST.get('last_name')
        
        # Asignar grupo
        if ugrupo:
            grupo = Group.objects.get(name=ugrupo)
            nuevo_u.groups.add(grupo)
        
        nuevo_u.save()
        return redirect('lista_usuarios')
        
    return render(request, 'gestion/usuarios_crear.html', {'grupos': grupos})

@login_required
@user_passes_test(es_admin)
def editar_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    grupos = Group.objects.all()
    
    if request.method == 'POST':
        usuario.first_name = request.POST.get('first_name')
        usuario.last_name = request.POST.get('last_name')
        usuario.username = request.POST.get('username')
        
        # Lógica de Activo/Retirado
        estatus = request.POST.get('is_active')
        usuario.is_active = True if estatus == '1' else False
        
        # Actualizar Grupo
        nuevo_grupo = request.POST.get('grupo')
        if nuevo_grupo:
            usuario.groups.clear()
            grupo = Group.objects.get(name=nuevo_grupo)
            usuario.groups.add(grupo)
            
        usuario.save()
        return redirect('lista_usuarios')
        
    return render(request, 'gestion/usuarios_editar.html', {'u': usuario, 'grupos': grupos})