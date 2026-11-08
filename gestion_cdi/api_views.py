from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from .models import (
    PersonalCDI,
    Paciente,
    Turno,
    RutaMaterna,
    PlanificacionFamiliar,
    ControlEndocrino,
    ControlRespiratorio,
    InventarioEquipo,
    TurnoGuardia,
    Comuna,
    SectorCPT,
    IndicadorPoblacionalASIC,
)
from .serializers import (
    PersonalCDISerializer,
    TurnoGuardiaSerializer,
    PacienteSerializer,
    TurnoSerializer,
    ControlEndocrinoSerializer,
    ControlRespiratorioSerializer,
    RutaMaternaSerializer,
    PlanificacionFamiliarSerializer,
    InventarioEquipoSerializer,
    ComunaSerializer,
    SectorCPTSerializer,
    IndicadorPoblacionalASICSerializer,
    SyncBatchRequestSerializer,
)


# ==========================================
# 1. CONTROL ADMINISTRATIVO DE PERSONAL Y GUARDIAS
# ==========================================
@extend_schema_view(
    list=extend_schema(tags=['1. RRHH y Guardias']),
    retrieve=extend_schema(tags=['1. RRHH y Guardias']),
    create=extend_schema(tags=['1. RRHH y Guardias']),
    update=extend_schema(tags=['1. RRHH y Guardias']),
    partial_update=extend_schema(tags=['1. RRHH y Guardias']),
    destroy=extend_schema(tags=['1. RRHH y Guardias']),
)
class PersonalCDIViewSet(viewsets.ModelViewSet):
    """Gestión del talento humano del CDI El Llanito (Médicos, Enfermeros, Administrativos, etc.)."""
    queryset = PersonalCDI.objects.all().order_by('apellido', 'nombre')
    serializer_class = PersonalCDISerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['cedula', 'nombre', 'apellido', 'rol_profesional', 'especialidad', 'estatus']
    ordering_fields = ['cedula', 'apellido', 'fecha_ingreso']


@extend_schema_view(
    list=extend_schema(tags=['1. RRHH y Guardias']),
    retrieve=extend_schema(tags=['1. RRHH y Guardias']),
    create=extend_schema(tags=['1. RRHH y Guardias']),
    update=extend_schema(tags=['1. RRHH y Guardias']),
    partial_update=extend_schema(tags=['1. RRHH y Guardias']),
    destroy=extend_schema(tags=['1. RRHH y Guardias']),
)
class TurnoGuardiaViewSet(viewsets.ModelViewSet):
    """Control de guardias, turnos laborales y asistencia del personal del CDI."""
    queryset = TurnoGuardia.objects.select_related('personal', 'suplente').all()
    serializer_class = TurnoGuardiaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['personal__nombre', 'personal__apellido', 'personal__cedula', 'area_servicio', 'tipo_turno', 'estado']
    ordering_fields = ['fecha', 'tipo_turno', 'estado']


# ==========================================
# 2. PADRÓN DE PACIENTES Y COLA DE TURNOS
# ==========================================
@extend_schema_view(
    list=extend_schema(tags=['2. Pacientes y Cola de Turnos']),
    retrieve=extend_schema(tags=['2. Pacientes y Cola de Turnos']),
    create=extend_schema(tags=['2. Pacientes y Cola de Turnos']),
    update=extend_schema(tags=['2. Pacientes y Cola de Turnos']),
    partial_update=extend_schema(tags=['2. Pacientes y Cola de Turnos']),
    destroy=extend_schema(tags=['2. Pacientes y Cola de Turnos']),
)
class PacienteViewSet(viewsets.ModelViewSet):
    """Padrón general de pacientes adscritos al CDI El Llanito."""
    queryset = Paciente.objects.select_related('comuna', 'sector_cpt').all().order_by('-fecha_registro')
    serializer_class = PacienteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['=cedula', '^cedula', 'nombre', 'apellido', 'telefono', 'asic', 'direccion', 'alergias', 'antecedentes_personales']
    ordering_fields = ['cedula', 'apellido', 'fecha_registro']

    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.query_params
        sexo = params.get('sexo')
        comuna = params.get('comuna')
        sector_cpt = params.get('sector_cpt')
        grupo_sanguineo = params.get('grupo_sanguineo')
        gestante = params.get('gestante')
        posee_discapacidad = params.get('posee_discapacidad')

        if sexo:
            qs = qs.filter(sexo=sexo)
        if comuna:
            qs = qs.filter(comuna_id=comuna)
        if sector_cpt:
            qs = qs.filter(sector_cpt_id=sector_cpt)
        if grupo_sanguineo:
            qs = qs.filter(grupo_sanguineo=grupo_sanguineo)
        if gestante in ('true', 'True', '1'):
            qs = qs.filter(gestante=True)
        if posee_discapacidad in ('true', 'True', '1'):
            qs = qs.filter(posee_discapacidad=True)
        return qs

    @extend_schema(
        tags=['2. Pacientes y Cola de Turnos'],
        summary="Búsqueda rápida / Autocompletado de pacientes (Typeahead / TomSelect)",
        parameters=[
            OpenApiParameter(name='q', description='Cédula, nombre, apellido o teléfono del paciente', required=False, type=str),
            OpenApiParameter(name='limit', description='Cantidad máxima de resultados (por defecto 15)', required=False, type=int),
        ],
    )
    @action(detail=False, methods=['get'], url_path='autocompletar')
    def autocompletar(self, request):
        q = request.query_params.get('q', '').strip()
        try:
            limit = min(int(request.query_params.get('limit', 15)), 50)
        except ValueError:
            limit = 15

        qs = Paciente.objects.select_related('comuna', 'sector_cpt')
        if q:
            terminos = q.split()
            for termino in terminos:
                qs = qs.filter(
                    Q(cedula__icontains=termino) |
                    Q(nombre__icontains=termino) |
                    Q(apellido__icontains=termino) |
                    Q(telefono__icontains=termino)
                )

        resultados = []
        for p in qs[:limit]:
            resultados.append({
                'cedula': p.cedula,
                'tipo_cedula': p.tipo_cedula,
                'documento': f"{p.tipo_cedula}-{p.cedula}",
                'nombre_completo': f"{p.nombre} {p.apellido}",
                'texto_busqueda': f"{p.tipo_cedula}-{p.cedula} | {p.nombre} {p.apellido} ({p.edad})",
                'edad': p.edad,
                'sexo': p.sexo,
                'grupo_sanguineo': p.grupo_sanguineo,
                'alergias': p.alergias or 'Ninguna conocida',
                'antecedentes_personales': p.antecedentes_personales or 'Sin antecedentes registrados',
                'prioridad_sugerida_triaje': p.prioridad_sugerida_triaje,
                'sector': p.sector_cpt.nombre if p.sector_cpt else p.asic,
            })
        return Response({'resultados': resultados})

    @extend_schema(
        tags=['2. Pacientes y Cola de Turnos'],
        summary="Consultar expediente clínico integral del paciente (4 Programas + Turnos)",
    )
    @action(detail=True, methods=['get'], url_path='expediente')
    def expediente(self, request, pk=None):
        paciente = self.get_object()
        return Response({
            'ficha_admision': PacienteSerializer(paciente).data,
            'turnos': TurnoSerializer(paciente.turnos.all(), many=True).data,
            'programas_salud': {
                'endocrino_metabolico': ControlEndocrinoSerializer(paciente.controlendocrino_set.all(), many=True).data,
                'salud_respiratoria': ControlRespiratorioSerializer(paciente.controles_respiratorios.all(), many=True).data,
                'ruta_materna': RutaMaternaSerializer(paciente.rutamaterna_set.all(), many=True).data,
                'educacion_sexual': PlanificacionFamiliarSerializer(paciente.planificacionfamiliar_set.all(), many=True).data,
            },
        })


@extend_schema_view(
    list=extend_schema(tags=['2. Pacientes y Cola de Turnos']),
    retrieve=extend_schema(tags=['2. Pacientes y Cola de Turnos']),
    create=extend_schema(tags=['2. Pacientes y Cola de Turnos']),
    update=extend_schema(tags=['2. Pacientes y Cola de Turnos']),
    partial_update=extend_schema(tags=['2. Pacientes y Cola de Turnos']),
    destroy=extend_schema(tags=['2. Pacientes y Cola de Turnos']),
)
class TurnoViewSet(viewsets.ModelViewSet):
    """Gestión de la Cola de Turnos de Atención para Triaje y Programas de Salud."""
    queryset = Turno.objects.select_related('paciente', 'atendido_por').all()
    serializer_class = TurnoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['codigo_turno', 'paciente__cedula', 'paciente__nombre', 'paciente__apellido', 'programa', 'estado']
    ordering_fields = ['fecha_hora_llegada', 'prioridad', 'estado']

    @extend_schema(tags=['2. Pacientes y Cola de Turnos'], summary="Listar turnos en espera activa")
    @action(detail=False, methods=['get'], url_path='en-espera')
    def en_espera(self, request):
        turnos = self.get_queryset().filter(estado__in=['En Espera', 'Llamado', 'En Atención'])
        serializer = self.get_serializer(turnos, many=True)
        return Response(serializer.data)

    @extend_schema(tags=['2. Pacientes y Cola de Turnos'], summary="Marcar turno como atendido")
    @action(detail=True, methods=['post'], url_path='marcar-atendido')
    def marcar_atendido(self, request, pk=None):
        turno = self.get_object()
        turno.estado = 'Atendido'
        turno.fecha_hora_atencion = timezone.now()
        turno.save(update_fields=['estado', 'fecha_hora_atencion'])
        return Response(self.get_serializer(turno).data)


# ==========================================
# 3. LOS 4 PROGRAMAS DE SALUD AUTORIZADOS
# ==========================================
@extend_schema_view(
    list=extend_schema(tags=['3. Programas de Salud']),
    retrieve=extend_schema(tags=['3. Programas de Salud']),
    create=extend_schema(tags=['3. Programas de Salud']),
    update=extend_schema(tags=['3. Programas de Salud']),
    partial_update=extend_schema(tags=['3. Programas de Salud']),
    destroy=extend_schema(tags=['3. Programas de Salud']),
)
class ControlEndocrinoViewSet(viewsets.ModelViewSet):
    """Programa 1: Salud Endocrino-Metabólica."""
    queryset = ControlEndocrino.objects.select_related('paciente').all().order_by('-fecha_atencion')
    serializer_class = ControlEndocrinoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['paciente__cedula', 'paciente__nombre', 'paciente__apellido', 'diagnostico', 'pas']
    ordering_fields = ['fecha_atencion']


@extend_schema_view(
    list=extend_schema(tags=['3. Programas de Salud']),
    retrieve=extend_schema(tags=['3. Programas de Salud']),
    create=extend_schema(tags=['3. Programas de Salud']),
    update=extend_schema(tags=['3. Programas de Salud']),
    partial_update=extend_schema(tags=['3. Programas de Salud']),
    destroy=extend_schema(tags=['3. Programas de Salud']),
)
class ControlRespiratorioViewSet(viewsets.ModelViewSet):
    """Programa 2: Salud Respiratoria (Asma, EPOC, IRA, Sintomático Respiratorio/TB)."""
    queryset = ControlRespiratorio.objects.select_related('paciente', 'atendido_por').all().order_by('-fecha_atencion')
    serializer_class = ControlRespiratorioSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['paciente__cedula', 'paciente__nombre', 'paciente__apellido', 'diagnostico', 'pas']
    ordering_fields = ['fecha_atencion']


@extend_schema_view(
    list=extend_schema(tags=['3. Programas de Salud']),
    retrieve=extend_schema(tags=['3. Programas de Salud']),
    create=extend_schema(tags=['3. Programas de Salud']),
    update=extend_schema(tags=['3. Programas de Salud']),
    partial_update=extend_schema(tags=['3. Programas de Salud']),
    destroy=extend_schema(tags=['3. Programas de Salud']),
)
class RutaMaternaViewSet(viewsets.ModelViewSet):
    """Programa 3: Ruta Materna y Control Prenatal."""
    queryset = RutaMaterna.objects.select_related('paciente', 'atendido_por').all().order_by('-fecha_control')
    serializer_class = RutaMaternaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['paciente__cedula', 'paciente__nombre', 'paciente__apellido', 'eje', 'observaciones']
    ordering_fields = ['fecha_control', 'semanas_embarazo']


@extend_schema_view(
    list=extend_schema(tags=['3. Programas de Salud']),
    retrieve=extend_schema(tags=['3. Programas de Salud']),
    create=extend_schema(tags=['3. Programas de Salud']),
    update=extend_schema(tags=['3. Programas de Salud']),
    partial_update=extend_schema(tags=['3. Programas de Salud']),
    destroy=extend_schema(tags=['3. Programas de Salud']),
)
class PlanificacionFamiliarViewSet(viewsets.ModelViewSet):
    """Programa 4: Educación Sexual y Planificación Familiar."""
    queryset = PlanificacionFamiliar.objects.select_related('paciente').all().order_by('-fecha_atencion')
    serializer_class = PlanificacionFamiliarSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['paciente__cedula', 'paciente__nombre', 'paciente__apellido', 'metodo_entregado', 'primera_sucesiva']
    ordering_fields = ['fecha_atencion', 'semana']


# ==========================================
# 4. CONTROL DE EQUIPOS TECNOLÓGICOS
# ==========================================
@extend_schema_view(
    list=extend_schema(tags=['4. Inventario Tecnológico']),
    retrieve=extend_schema(tags=['4. Inventario Tecnológico']),
    create=extend_schema(tags=['4. Inventario Tecnológico']),
    update=extend_schema(tags=['4. Inventario Tecnológico']),
    partial_update=extend_schema(tags=['4. Inventario Tecnológico']),
    destroy=extend_schema(tags=['4. Inventario Tecnológico']),
)
class InventarioEquipoViewSet(viewsets.ModelViewSet):
    """Control de bienes nacionales y equipos médicos/tecnológicos del CDI."""
    queryset = InventarioEquipo.objects.select_related('responsable').all().order_by('codigo_bien_nacional')
    serializer_class = InventarioEquipoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['codigo_bien_nacional', 'nombre_equipo', 'tipo_equipo', 'ubicacion_especifica', 'estado_fisico']
    ordering_fields = ['codigo_bien_nacional', 'nombre_equipo', 'estado_fisico']


# ==========================================
# 5. ESTADÍSTICAS POBLACIONALES Y TERRITORIO
# ==========================================
@extend_schema_view(
    list=extend_schema(tags=['5. Estadísticas Poblacionales (ASIC)']),
    retrieve=extend_schema(tags=['5. Estadísticas Poblacionales (ASIC)']),
    create=extend_schema(tags=['5. Estadísticas Poblacionales (ASIC)']),
    update=extend_schema(tags=['5. Estadísticas Poblacionales (ASIC)']),
    partial_update=extend_schema(tags=['5. Estadísticas Poblacionales (ASIC)']),
    destroy=extend_schema(tags=['5. Estadísticas Poblacionales (ASIC)']),
)
class ComunaViewSet(viewsets.ModelViewSet):
    """Comunas adscritas al ámbito territorial del ASIC El Llanito."""
    queryset = Comuna.objects.prefetch_related('sectores').all()
    serializer_class = ComunaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['orden', 'nombre']


@extend_schema_view(
    list=extend_schema(tags=['5. Estadísticas Poblacionales (ASIC)']),
    retrieve=extend_schema(tags=['5. Estadísticas Poblacionales (ASIC)']),
    create=extend_schema(tags=['5. Estadísticas Poblacionales (ASIC)']),
    update=extend_schema(tags=['5. Estadísticas Poblacionales (ASIC)']),
    partial_update=extend_schema(tags=['5. Estadísticas Poblacionales (ASIC)']),
    destroy=extend_schema(tags=['5. Estadísticas Poblacionales (ASIC)']),
)
class SectorCPTViewSet(viewsets.ModelViewSet):
    """Consultorios Populares (CPT) y sectores de salud del ASIC."""
    queryset = SectorCPT.objects.select_related('comuna').all()
    serializer_class = SectorCPTSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'comuna__nombre', 'medico_responsable', 'situacion_espacio']
    ordering_fields = ['numero', 'poblacion', 'familias']


@extend_schema_view(
    list=extend_schema(tags=['5. Estadísticas Poblacionales (ASIC)']),
    retrieve=extend_schema(tags=['5. Estadísticas Poblacionales (ASIC)']),
    create=extend_schema(tags=['5. Estadísticas Poblacionales (ASIC)']),
    update=extend_schema(tags=['5. Estadísticas Poblacionales (ASIC)']),
    partial_update=extend_schema(tags=['5. Estadísticas Poblacionales (ASIC)']),
    destroy=extend_schema(tags=['5. Estadísticas Poblacionales (ASIC)']),
)
class IndicadorPoblacionalASICViewSet(viewsets.ModelViewSet):
    """Indicadores demográficos globales de la pizarra del ASIC El Llanito."""
    queryset = IndicadorPoblacionalASIC.objects.all()
    serializer_class = IndicadorPoblacionalASICSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['5. Estadísticas Poblacionales (ASIC)'],
        summary="Resumen estadístico integral del CDI El Llanito (Demografía, 4 Programas, Turnos e Inventario)",
    )
    @action(detail=False, methods=['get'], url_path='resumen-integral')
    def resumen_integral(self, request):
        indicador = IndicadorPoblacionalASIC.objects.first()
        return Response({
            'pizarra_asic': IndicadorPoblacionalASICSerializer(indicador).data if indicador else None,
            'padron_pacientes': {
                'total_registrados': Paciente.objects.count(),
                'femenino': Paciente.objects.filter(sexo='F').count(),
                'masculino': Paciente.objects.filter(sexo='M').count(),
                'gestantes': Paciente.objects.filter(gestante=True).count(),
                'con_discapacidad': Paciente.objects.filter(posee_discapacidad=True).count(),
            },
            'cola_turnos': {
                'en_espera': Turno.objects.filter(estado='En Espera').count(),
                'en_atencion': Turno.objects.filter(estado__in=['Llamado', 'En Atención']).count(),
                'atendidos_total': Turno.objects.filter(estado='Atendido').count(),
            },
            'programas_salud': {
                'endocrino_metabolico': {
                    'total_controles': ControlEndocrino.objects.count(),
                    'diabetes_mellitus': ControlEndocrino.objects.filter(diabetes_mellitus=True).count(),
                    'hipertension_arterial': ControlEndocrino.objects.filter(hipertension_arterial=True).count(),
                    'pie_diabetico': ControlEndocrino.objects.filter(pie_diabetico=True).count(),
                },
                'salud_respiratoria': {
                    'total_controles': ControlRespiratorio.objects.count(),
                    'asma_bronquial': ControlRespiratorio.objects.filter(asma_bronquial=True).count(),
                    'ira': ControlRespiratorio.objects.filter(infeccion_respiratoria_aguda=True).count(),
                    'nebulizaciones': ControlRespiratorio.objects.filter(nebulizacion_realizada=True).count(),
                },
                'ruta_materna': {
                    'total_controles': RutaMaterna.objects.count(),
                },
                'educacion_sexual': {
                    'total_controles': PlanificacionFamiliar.objects.count(),
                },
            },
            'inventario_equipos': {
                'total': InventarioEquipo.objects.count(),
                'operativos': InventarioEquipo.objects.filter(estado_fisico='Operativo').count(),
                'en_reparacion': InventarioEquipo.objects.filter(estado_fisico='En Reparación').count(),
                'danados': InventarioEquipo.objects.filter(estado_fisico='Dañado').count(),
            },
            'rrhh': {
                'personal_activo': PersonalCDI.objects.filter(estatus='Activo').count(),
                'guardias_en_curso': TurnoGuardia.objects.filter(estado='En Curso').count(),
            },
        })


# ==========================================
# 6. SINCRONIZACIÓN DIFERIDA (OFFLINE-FIRST)
# ==========================================
class SyncBatchAPIView(APIView):
    """
    Endpoint Offline-First (`/api/v1/sync/batch/`) para sincronizar lotes de pacientes,
    turnos y controles clínicos registrados sin conexión a internet.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['6. Sincronización Offline-First'],
        summary="Sincronización diferida por lotes (Batch Sync)",
        request=SyncBatchRequestSerializer,
        responses={201: dict},
    )
    def post(self, request):
        resumen = {
            'pacientes_sincronizados': 0,
            'turnos_sincronizados': 0,
            'controles_endocrinos_sincronizados': 0,
            'controles_respiratorios_sincronizados': 0,
            'rutas_maternas_sincronizadas': 0,
            'planificacion_familiar_sincronizada': 0,
            'errores': [],
        }

        data = request.data
        with transaction.atomic():
            # 1. Sincronizar Pacientes (upsert por cédula)
            for idx, pac_data in enumerate(data.get('pacientes', [])):
                cedula = pac_data.get('cedula')
                if not cedula:
                    resumen['errores'].append({'entidad': 'pacientes', 'indice': idx, 'error': 'Cédula requerida'})
                    continue
                instancia = Paciente.objects.filter(cedula=cedula).first()
                serializer = PacienteSerializer(instance=instancia, data=pac_data, partial=bool(instancia))
                if serializer.is_valid():
                    serializer.save()
                    resumen['pacientes_sincronizados'] += 1
                else:
                    resumen['errores'].append({'entidad': 'pacientes', 'cedula': cedula, 'error': serializer.errors})

            # 2. Sincronizar Cola de Turnos y los 4 Programas de Salud
            lotes_programas = [
                ('turnos', TurnoSerializer, 'turnos_sincronizados'),
                ('controles_endocrinos', ControlEndocrinoSerializer, 'controles_endocrinos_sincronizados'),
                ('controles_respiratorios', ControlRespiratorioSerializer, 'controles_respiratorios_sincronizados'),
                ('rutas_maternas', RutaMaternaSerializer, 'rutas_maternas_sincronizadas'),
                ('planificacion_familiar', PlanificacionFamiliarSerializer, 'planificacion_familiar_sincronizada'),
            ]

            for clave_json, serializer_cls, clave_resumen in lotes_programas:
                for idx, item_data in enumerate(data.get(clave_json, [])):
                    serializer = serializer_cls(data=item_data)
                    if serializer.is_valid():
                        serializer.save()
                        resumen[clave_resumen] += 1
                    else:
                        resumen['errores'].append({
                            'entidad': clave_json,
                            'indice': idx,
                            'error': serializer.errors,
                        })

        http_status = status.HTTP_207_MULTI_STATUS if resumen['errores'] else status.HTTP_201_CREATED
        return Response(
            {
                'mensaje': 'Proceso de sincronización diferida completado.',
                'timestamp_servidor': timezone.now(),
                'resumen': resumen,
            },
            status=http_status,
        )

