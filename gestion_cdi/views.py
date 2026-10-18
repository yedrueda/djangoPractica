from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum # Para búsquedas avanzadas y sumas
from .models import (
    Paciente, PersonalCDI, InventarioEquipo, ControlEndocrino, 
    RutaMaterna, PlanificacionFamiliar, TurnoGuardia, 
    Comuna, SectorCPT, IndicadorPoblacionalASIC
)
from .forms import (
    PacienteForm, PersonalCDIForm, InventarioEquipoForm, 
    ControlEndocrinoForm, RutaMaternaForm, PlanificacionFamiliarForm, TurnoGuardiaForm,
    SectorCPTForm, IndicadorPoblacionalForm
)

@login_required
def inicio(request):
    hoy = date.today()
    total_pacientes = Paciente.objects.count()
    total_personal = PersonalCDI.objects.count()
    total_equipos = InventarioEquipo.objects.count()
    total_consultas = ControlEndocrino.objects.count() 
    guardias_hoy = TurnoGuardia.objects.filter(fecha=hoy).select_related('personal')
    total_guardias_hoy = guardias_hoy.count()

    contexto = {
        'total_pacientes': total_pacientes,
        'total_personal': total_personal,
        'total_equipos': total_equipos,
        'total_consultas': total_consultas,
        'guardias_hoy': guardias_hoy,
        'total_guardias_hoy': total_guardias_hoy,
        'hoy': hoy,
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
    return render(request, 'gestion_cdi/editar_personal.html', {'form': form, 'personal': personal, 'empleado': personal})    
               
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


@login_required
def seleccionar_programa(request):
    """Vista para la sala de triaje virtual (menú de los 3 botones)"""
    return render(request, 'gestion_cdi/seleccionar_programa.html')

@login_required
def crear_control_endocrino(request):
    if request.method == 'POST':
        form = ControlEndocrinoForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.save()
            return redirect('lista_consultas') 
    else:
        # Cuando entras por primera vez (GET), se ejecuta esto:
        form = ControlEndocrinoForm()
    
    # Confirma que la ruta del archivo HTML aquí esté bien escrita:
    return render(request, 'gestion_cdi/crear_control_endocrino.html', {'form': form})

# 1. VER DETALLES (LA HOJA MÉDICA)
@login_required
def detalle_control_endocrino(request, pk):
    consulta = get_object_or_404(ControlEndocrino, pk=pk)
    return render(request, 'gestion_cdi/detalle_control_endocrino.html', {'consulta': consulta})

# 2. EDITAR CONSULTA
@login_required
def editar_control_endocrino(request, pk):
    consulta = get_object_or_404(ControlEndocrino, pk=pk)
    if request.method == 'POST':
        form = ControlEndocrinoForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            return redirect('lista_consultas')
    else:
        form = ControlEndocrinoForm(instance=consulta)
    
    # Reutilizamos la misma plantilla de creación, pasándole el formulario lleno
    return render(request, 'gestion_cdi/crear_control_endocrino.html', {'form': form, 'editando': True})

# 3. ELIMINAR CONSULTA
@login_required
def eliminar_control_endocrino(request, pk):
    consulta = get_object_or_404(ControlEndocrino, pk=pk)
    # Al procesar la confirmación nativa de JS del paso 1, borramos directamente
    consulta.delete()
    return redirect('lista_consultas')

@login_required
def crear_ruta_materna(request):
    """Vista para el formulario de Ruta Materna"""
    if request.method == 'POST':
        form = RutaMaternaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_consultas')
    else:
        form = RutaMaternaForm()
    return render(request, 'gestion_cdi/crear_ruta_materna.html', {'form': form})

@login_required
def crear_planificacion_familiar(request):
    """Vista para el formulario de Planificación Familiar"""
    if request.method == 'POST':
        form = PlanificacionFamiliarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_consultas')
    else:
        form = PlanificacionFamiliarForm()
    return render(request, 'gestion_cdi/crear_planificacion_familiar.html', {'form': form})

@login_required
def lista_consultas(request):
    # 1. Capturamos el parámetro 'buscar' enviado desde el formulario HTML
    busqueda = request.GET.get('buscar', '')
    
    # 2. Obtenemos todas las consultas ordenadas de la más reciente a la más antigua
    consultas = ControlEndocrino.objects.all().order_by('-fecha_atencion')
    
    # 3. Si el usuario escribió algo, filtramos por Cédula, Nombre o Apellido del paciente
    if busqueda:
        consultas = consultas.filter(
            Q(paciente__cedula__icontains=busqueda) |
            Q(paciente__nombre__icontains=busqueda) |
            Q(paciente__apellido__icontains=busqueda)
        )
    
    # 4. Pasamos las consultas filtradas y el término de búsqueda actual a la plantilla
    return render(request, 'gestion_cdi/lista_consultas.html', {
        'consultas': consultas,
        'busqueda': busqueda
    })

# ==========================================
# 5. MÓDULO DE TURNOS Y GUARDIAS DEL PERSONAL
# ==========================================

@login_required
def lista_guardias(request):
    fecha_filtro = request.GET.get('fecha', '')
    estado_filtro = request.GET.get('estado', '')
    area_filtro = request.GET.get('area', '')
    busqueda = request.GET.get('buscar', '')

    guardias = TurnoGuardia.objects.select_related('personal', 'suplente').all()

    if fecha_filtro:
        guardias = guardias.filter(fecha=fecha_filtro)
    if estado_filtro:
        guardias = guardias.filter(estado=estado_filtro)
    if area_filtro:
        guardias = guardias.filter(area_servicio=area_filtro)
    if busqueda:
        guardias = guardias.filter(
            Q(personal__nombre__icontains=busqueda) |
            Q(personal__apellido__icontains=busqueda) |
            Q(personal__cedula__icontains=busqueda) |
            Q(observaciones__icontains=busqueda)
        )

    hoy = date.today()
    total_hoy = TurnoGuardia.objects.filter(fecha=hoy).count()
    total_en_curso = TurnoGuardia.objects.filter(estado='En Curso').count()
    total_programadas = TurnoGuardia.objects.filter(estado='Programada').count()

    contexto = {
        'guardias': guardias,
        'fecha_filtro': fecha_filtro,
        'estado_filtro': estado_filtro,
        'area_filtro': area_filtro,
        'busqueda': busqueda,
        'hoy': hoy,
        'total_hoy': total_hoy,
        'total_en_curso': total_en_curso,
        'total_programadas': total_programadas,
        'areas_disponibles': TurnoGuardia.AREAS,
        'estados_disponibles': TurnoGuardia.ESTADOS,
    }
    return render(request, 'gestion_cdi/lista_guardias.html', contexto)

@login_required
def crear_guardia(request):
    if request.method == 'POST':
        form = TurnoGuardiaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_guardias')
    else:
        fecha_inicial = request.GET.get('fecha', str(date.today()))
        form = TurnoGuardiaForm(initial={'fecha': fecha_inicial})
    return render(request, 'gestion_cdi/crear_guardia.html', {'form': form})

@login_required
def editar_guardia(request, id):
    guardia = get_object_or_404(TurnoGuardia, id=id)
    if request.method == 'POST':
        form = TurnoGuardiaForm(request.POST, instance=guardia)
        if form.is_valid():
            form.save()
            return redirect('lista_guardias')
    else:
        form = TurnoGuardiaForm(instance=guardia)
    return render(request, 'gestion_cdi/editar_guardia.html', {'form': form, 'guardia': guardia})

@login_required
def borrar_guardia(request, id):
    guardia = get_object_or_404(TurnoGuardia, id=id)
    if request.method == 'POST':
        guardia.delete()
        return redirect('lista_guardias')
    return render(request, 'gestion_cdi/borrar_guardia.html', {'guardia': guardia})

# ==========================================
# 6. MÓDULO POBLACIONAL Y COMUNAL (ASIC)
# ==========================================

@login_required
def resumen_poblacional(request):
    indicador = IndicadorPoblacionalASIC.objects.first()
    if not indicador:
        indicador = IndicadorPoblacionalASIC.objects.create(
            poblacion_total=54975,
            familias_total=15180,
            comunas_total=8,
            femenino_total=28023,
            masculino_total=26952,
            red_referencia="CEO, Hospital Dr. Domingo Luciani, Clínica Popular Mesuca, CPT3 El Carmen"
        )

    # Conteo de pacientes reales registrados en base de datos
    total_pacientes_bd = Paciente.objects.count()
    pacientes_fem = Paciente.objects.filter(sexo='F').count()
    pacientes_masc = Paciente.objects.filter(sexo='M').count()

    # Porcentajes globales
    porc_femenino = round((indicador.femenino_total / indicador.poblacion_total) * 100, 1) if indicador.poblacion_total else 0
    porc_masculino = round((indicador.masculino_total / indicador.poblacion_total) * 100, 1) if indicador.poblacion_total else 0

    # Comunas con sus CPTs
    comunas = Comuna.objects.prefetch_related('sectores').all()
    
    # Filtros
    comuna_id = request.GET.get('comuna', '')
    busqueda = request.GET.get('buscar', '')

    sectores = SectorCPT.objects.select_related('comuna').all()
    if comuna_id:
        sectores = sectores.filter(comuna_id=comuna_id)
    if busqueda:
        sectores = sectores.filter(
            Q(nombre__icontains=busqueda) |
            Q(medico_responsable__icontains=busqueda) |
            Q(situacion_espacio__icontains=busqueda) |
            Q(comuna__nombre__icontains=busqueda)
        )

    totales_cpt = SectorCPT.objects.aggregate(
        total_pob=Sum('poblacion'),
        total_fam=Sum('familias')
    )

    contexto = {
        'indicador': indicador,
        'porc_femenino': porc_femenino,
        'porc_masculino': porc_masculino,
        'total_pacientes_bd': total_pacientes_bd,
        'pacientes_fem': pacientes_fem,
        'pacientes_masc': pacientes_masc,
        'comunas': comunas,
        'sectores': sectores,
        'comuna_id': comuna_id,
        'busqueda': busqueda,
        'totales_cpt': totales_cpt,
    }
    return render(request, 'gestion_cdi/resumen_poblacional.html', contexto)

@login_required
def crear_sector_cpt(request):
    if request.method == 'POST':
        form = SectorCPTForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('resumen_poblacional')
    else:
        comuna_inicial = request.GET.get('comuna')
        form = SectorCPTForm(initial={'comuna': comuna_inicial} if comuna_inicial else None)
    return render(request, 'gestion_cdi/crear_sector_cpt.html', {'form': form})

@login_required
def editar_sector_cpt(request, id):
    sector = get_object_or_404(SectorCPT, id=id)
    if request.method == 'POST':
        form = SectorCPTForm(request.POST, instance=sector)
        if form.is_valid():
            form.save()
            return redirect('resumen_poblacional')
    else:
        form = SectorCPTForm(instance=sector)
    return render(request, 'gestion_cdi/editar_sector_cpt.html', {'form': form, 'sector': sector})

@login_required
def borrar_sector_cpt(request, id):
    sector = get_object_or_404(SectorCPT, id=id)
    if request.method == 'POST':
        sector.delete()
        return redirect('resumen_poblacional')
    return render(request, 'gestion_cdi/borrar_sector_cpt.html', {'sector': sector})

@login_required
def editar_indicadores_poblacionales(request):
    indicador = IndicadorPoblacionalASIC.objects.first()
    if not indicador:
        indicador = IndicadorPoblacionalASIC.objects.create()
    if request.method == 'POST':
        form = IndicadorPoblacionalForm(request.POST, instance=indicador)
        if form.is_valid():
            form.save()
            return redirect('resumen_poblacional')
    else:
        form = IndicadorPoblacionalForm(instance=indicador)
    return render(request, 'gestion_cdi/editar_indicadores_poblacionales.html', {'form': form, 'indicador': indicador})

