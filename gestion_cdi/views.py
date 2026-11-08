from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Sum # Para búsquedas avanzadas y sumas
from .models import (
    Paciente, PersonalCDI, InventarioEquipo, ControlEndocrino, ControlRespiratorio,
    RutaMaterna, PlanificacionFamiliar, TurnoGuardia, 
    Comuna, SectorCPT, IndicadorPoblacionalASIC
)
from .forms import (
    PacienteForm, PersonalCDIForm, InventarioEquipoForm, 
    ControlEndocrinoForm, ControlRespiratorioForm, RutaMaternaForm, PlanificacionFamiliarForm, TurnoGuardiaForm,
    SectorCPTForm, IndicadorPoblacionalForm
)

@login_required
def inicio(request):
    hoy = date.today()
    total_pacientes = Paciente.objects.count()
    total_personal = PersonalCDI.objects.count()
    total_equipos = InventarioEquipo.objects.count()
    total_consultas = (
        ControlEndocrino.objects.count() +
        ControlRespiratorio.objects.count() +
        RutaMaterna.objects.count() +
        PlanificacionFamiliar.objects.count()
    )
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

# Vista para listar pacientes con búsqueda avanzada, filtros y paginación
@login_required
def lista_pacientes(request):
    busqueda = request.GET.get('buscar', '').strip()
    sexo_filtro = request.GET.get('sexo', '').strip()
    comuna_filtro = request.GET.get('comuna', '').strip()
    condicion_filtro = request.GET.get('condicion', '').strip()

    pacientes_qs = Paciente.objects.select_related('comuna', 'sector_cpt').all().order_by('-fecha_registro')

    if busqueda:
        for termino in busqueda.split():
            pacientes_qs = pacientes_qs.filter(
                Q(cedula__icontains=termino) |
                Q(nombre__icontains=termino) |
                Q(apellido__icontains=termino) |
                Q(telefono__icontains=termino) |
                Q(direccion__icontains=termino) |
                Q(sector_cpt__nombre__icontains=termino)
            )

    if sexo_filtro:
        pacientes_qs = pacientes_qs.filter(sexo=sexo_filtro)
    if comuna_filtro:
        pacientes_qs = pacientes_qs.filter(comuna_id=comuna_filtro)
    if condicion_filtro == 'gestante':
        pacientes_qs = pacientes_qs.filter(gestante=True)
    elif condicion_filtro == 'discapacidad':
        pacientes_qs = pacientes_qs.filter(posee_discapacidad=True)
    elif condicion_filtro == 'adulto_mayor':
        hoy = date.today()
        fecha_corte = date(hoy.year - 60, hoy.month, hoy.day)
        pacientes_qs = pacientes_qs.filter(fecha_nacimiento__lte=fecha_corte)

    total_resultados = pacientes_qs.count()
    paginator = Paginator(pacientes_qs, 20)
    page_number = request.GET.get('page')
    pacientes_page = paginator.get_page(page_number)

    contexto = {
        'pacientes': pacientes_page,
        'total_resultados': total_resultados,
        'busqueda': busqueda,
        'sexo_filtro': sexo_filtro,
        'comuna_filtro': comuna_filtro,
        'condicion_filtro': condicion_filtro,
        'comunas': Comuna.objects.all(),
    }
    return render(request, 'gestion_cdi/lista_pacientes.html', contexto)

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
        paciente_cedula = request.GET.get('paciente')
        initial = {'paciente': paciente_cedula} if paciente_cedula else None
        form = ControlEndocrinoForm(initial=initial)
    
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

# ==========================================
# PROGRAMA 2: SALUD RESPIRATORIA
# ==========================================
@login_required
def crear_control_respiratorio(request):
    if request.method == 'POST':
        form = ControlRespiratorioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_consultas')
    else:
        paciente_cedula = request.GET.get('paciente')
        initial = {'paciente': paciente_cedula} if paciente_cedula else None
        form = ControlRespiratorioForm(initial=initial)
    return render(request, 'gestion_cdi/crear_control_respiratorio.html', {'form': form})

@login_required
def detalle_control_respiratorio(request, pk):
    consulta = get_object_or_404(ControlRespiratorio, pk=pk)
    return render(request, 'gestion_cdi/detalle_control_respiratorio.html', {'consulta': consulta})

@login_required
def editar_control_respiratorio(request, pk):
    consulta = get_object_or_404(ControlRespiratorio, pk=pk)
    if request.method == 'POST':
        form = ControlRespiratorioForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            return redirect('lista_consultas')
    else:
        form = ControlRespiratorioForm(instance=consulta)
    return render(request, 'gestion_cdi/crear_control_respiratorio.html', {'form': form, 'editando': True})

@login_required
def eliminar_control_respiratorio(request, pk):
    consulta = get_object_or_404(ControlRespiratorio, pk=pk)
    consulta.delete()
    return redirect('lista_consultas')

# ==========================================
# PROGRAMA 3: RUTA MATERNA
# ==========================================
@login_required
def crear_ruta_materna(request):
    """Vista para el formulario de Ruta Materna"""
    if request.method == 'POST':
        form = RutaMaternaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_consultas')
    else:
        paciente_cedula = request.GET.get('paciente')
        initial = {'paciente': paciente_cedula} if paciente_cedula else None
        form = RutaMaternaForm(initial=initial)
    return render(request, 'gestion_cdi/crear_ruta_materna.html', {'form': form})

@login_required
def detalle_ruta_materna(request, pk):
    consulta = get_object_or_404(RutaMaterna, pk=pk)
    return render(request, 'gestion_cdi/detalle_ruta_materna.html', {'consulta': consulta})

@login_required
def editar_ruta_materna(request, pk):
    consulta = get_object_or_404(RutaMaterna, pk=pk)
    if request.method == 'POST':
        form = RutaMaternaForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            return redirect('lista_consultas')
    else:
        form = RutaMaternaForm(instance=consulta)
    return render(request, 'gestion_cdi/crear_ruta_materna.html', {'form': form, 'editando': True})

@login_required
def eliminar_ruta_materna(request, pk):
    consulta = get_object_or_404(RutaMaterna, pk=pk)
    consulta.delete()
    return redirect('lista_consultas')

# ==========================================
# PROGRAMA 4: EDUCACIÓN SEXUAL Y PLANIFICACIÓN FAMILIAR
# ==========================================
@login_required
def crear_planificacion_familiar(request):
    """Vista para el formulario de Planificación Familiar"""
    if request.method == 'POST':
        form = PlanificacionFamiliarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_consultas')
    else:
        paciente_cedula = request.GET.get('paciente')
        initial = {'paciente': paciente_cedula} if paciente_cedula else None
        form = PlanificacionFamiliarForm(initial=initial)
    return render(request, 'gestion_cdi/crear_planificacion_familiar.html', {'form': form})

@login_required
def detalle_planificacion_familiar(request, pk):
    consulta = get_object_or_404(PlanificacionFamiliar, pk=pk)
    return render(request, 'gestion_cdi/detalle_planificacion_familiar.html', {'consulta': consulta})

@login_required
def editar_planificacion_familiar(request, pk):
    consulta = get_object_or_404(PlanificacionFamiliar, pk=pk)
    if request.method == 'POST':
        form = PlanificacionFamiliarForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            return redirect('lista_consultas')
    else:
        form = PlanificacionFamiliarForm(instance=consulta)
    return render(request, 'gestion_cdi/crear_planificacion_familiar.html', {'form': form, 'editando': True})

@login_required
def eliminar_planificacion_familiar(request, pk):
    consulta = get_object_or_404(PlanificacionFamiliar, pk=pk)
    consulta.delete()
    return redirect('lista_consultas')

@login_required
def lista_consultas(request):
    busqueda = request.GET.get('buscar', '').strip()
    programa_filtro = request.GET.get('programa', '').strip()

    def filtrar_por_paciente(qs):
        if not busqueda:
            return qs
        for termino in busqueda.split():
            qs = qs.filter(
                Q(paciente__cedula__icontains=termino) |
                Q(paciente__nombre__icontains=termino) |
                Q(paciente__apellido__icontains=termino)
            )
        return qs

    registros = []

    if programa_filtro in ('', 'endocrino'):
        for c in filtrar_por_paciente(ControlEndocrino.objects.select_related('paciente').all()):
            registros.append({
                'id': c.id,
                'fecha': c.fecha_atencion,
                'paciente': c.paciente,
                'programa_nombre': 'Endocrino-Metabólico',
                'programa_badge': 'bg-primary text-primary',
                'signo_1': f"T.A: {c.tension_arterial or '--'} mmHg",
                'signo_2': f"Glicemia: {c.glucemia_ayunas or '--'} mg/dL | IMC: {c.imc or '--'}",
                'diagnostico': c.diagnostico or 'Sin diagnóstico registrado',
                'url_detalle': 'detalle_control_endocrino',
                'url_editar': 'editar_control_endocrino',
                'url_eliminar': 'eliminar_control_endocrino',
            })

    if programa_filtro in ('', 'respiratorio'):
        for c in filtrar_por_paciente(ControlRespiratorio.objects.select_related('paciente').all()):
            registros.append({
                'id': c.id,
                'fecha': c.fecha_atencion,
                'paciente': c.paciente,
                'programa_nombre': 'Salud Respiratoria',
                'programa_badge': 'bg-info text-info',
                'signo_1': f"SpO2: {c.saturacion_oxigeno or '--'}% | F.R: {c.frecuencia_respiratoria or '--'} rpm",
                'signo_2': f"Severidad: {c.severidad_cuadro}",
                'diagnostico': c.diagnostico or 'Sin diagnóstico registrado',
                'url_detalle': 'detalle_control_respiratorio',
                'url_editar': 'editar_control_respiratorio',
                'url_eliminar': 'eliminar_control_respiratorio',
            })

    if programa_filtro in ('', 'materna'):
        for c in filtrar_por_paciente(RutaMaterna.objects.select_related('paciente').all()):
            registros.append({
                'id': c.id,
                'fecha': c.fecha_control,
                'paciente': c.paciente,
                'programa_nombre': 'Ruta Materna',
                'programa_badge': 'bg-danger text-danger',
                'signo_1': f"Gestación: {c.semanas_embarazo} sem ({c.formula_obstetrica})",
                'signo_2': f"FCF: {c.frecuencia_cardiaca_fetal or '--'} lpm | {c.riesgo_obstetrico}",
                'diagnostico': c.diagnostico or c.observaciones or 'Control prenatal registrado',
                'url_detalle': 'detalle_ruta_materna',
                'url_editar': 'editar_ruta_materna',
                'url_eliminar': 'eliminar_ruta_materna',
            })

    if programa_filtro in ('', 'planificacion'):
        for c in filtrar_por_paciente(PlanificacionFamiliar.objects.select_related('paciente').all()):
            registros.append({
                'id': c.id,
                'fecha': c.fecha_atencion,
                'paciente': c.paciente,
                'programa_nombre': 'Educación Sexual',
                'programa_badge': 'bg-success text-success',
                'signo_1': f"Método: {c.tipo_metodo}",
                'signo_2': f"Preservativos: {c.preservativo_masculino} | T.A: {c.tension_arterial or '--'}",
                'diagnostico': c.diagnostico or c.observaciones or 'Orientación en salud sexual',
                'url_detalle': 'detalle_planificacion_familiar',
                'url_editar': 'editar_planificacion_familiar',
                'url_eliminar': 'eliminar_planificacion_familiar',
            })

    registros.sort(key=lambda item: item['fecha'], reverse=True)

    return render(request, 'gestion_cdi/lista_consultas.html', {
        'consultas': ControlEndocrino.objects.select_related('paciente').all().order_by('-fecha_atencion'),
        'registros_unificados': registros,
        'busqueda': busqueda,
        'programa_filtro': programa_filtro,
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

