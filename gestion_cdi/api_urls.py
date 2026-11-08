from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .api_views import (
    PersonalCDIViewSet,
    TurnoGuardiaViewSet,
    PacienteViewSet,
    TurnoViewSet,
    ControlEndocrinoViewSet,
    ControlRespiratorioViewSet,
    RutaMaternaViewSet,
    PlanificacionFamiliarViewSet,
    InventarioEquipoViewSet,
    ComunaViewSet,
    SectorCPTViewSet,
    IndicadorPoblacionalASICViewSet,
    SyncBatchAPIView,
)

router = DefaultRouter()

# 1. Control Administrativo de Personal y Guardias
router.register(r'personal', PersonalCDIViewSet, basename='api-personal')
router.register(r'guardias', TurnoGuardiaViewSet, basename='api-guardias')

# 2. Padrón de Pacientes y Cola de Turnos
router.register(r'pacientes', PacienteViewSet, basename='api-pacientes')
router.register(r'turnos', TurnoViewSet, basename='api-turnos')

# 3. Los 4 Programas de Salud autorizados
router.register(r'programas/endocrino', ControlEndocrinoViewSet, basename='api-endocrino')
router.register(r'programas/respiratorio', ControlRespiratorioViewSet, basename='api-respiratorio')
router.register(r'programas/ruta-materna', RutaMaternaViewSet, basename='api-ruta-materna')
router.register(r'programas/planificacion-familiar', PlanificacionFamiliarViewSet, basename='api-planificacion-familiar')

# 4. Control de Equipos Tecnológicos
router.register(r'inventario', InventarioEquipoViewSet, basename='api-inventario')

# 5. Estadísticas Poblacionales y Territorio (ASIC)
router.register(r'comunas', ComunaViewSet, basename='api-comunas')
router.register(r'sectores-cpt', SectorCPTViewSet, basename='api-sectores-cpt')
router.register(r'indicadores-asic', IndicadorPoblacionalASICViewSet, basename='api-indicadores-asic')

urlpatterns = [
    # Autenticación JWT
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Sincronización Diferida (Offline-First)
    path('sync/batch/', SyncBatchAPIView.as_view(), name='api_sync_batch'),

    # Rutas generadas por el Router de ViewSets
    path('', include(router.urls)),
]

