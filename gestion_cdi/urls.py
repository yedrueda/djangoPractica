from django.urls import path
from django.contrib.auth import views as auth_views 
from . import views

urlpatterns = [
    # ==========================================
    # 1. AUTENTICACIÓN Y NAVEGACIÓN BASE
    # ==========================================
    path('login/', auth_views.LoginView.as_view(template_name='gestion_cdi/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.inicio, name='inicio'),
    
    # ==========================================
    # 2. MÓDULOS ADMINISTRATIVOS Y LOGÍSTICOS
    # ==========================================
    
    # Registro y Gestión de Pacientes
    path('pacientes/', views.lista_pacientes, name='lista_pacientes'),
    path('pacientes/nuevo/', views.crear_paciente, name='crear_paciente'),
    path('pacientes/editar/<int:cedula>/', views.editar_paciente, name='editar_paciente'),
    path('pacientes/borrar/<int:cedula>/', views.borrar_paciente, name='borrar_paciente'),

    # Gestión de Personal (Talento Humano del CDI)
    path('personal/', views.lista_personal, name='lista_personal'),
    path('personal/nuevo/', views.crear_personal, name='crear_personal'),
    path('personal/editar/<int:cedula>/', views.editar_personal, name='editar_personal'),
    path('personal/borrar/<int:cedula>/', views.borrar_personal, name='borrar_personal'),

    # Inventario Físico (Equipos Médicos y Tecnológicos)
    path('inventario/', views.lista_equipos, name='lista_equipos'),
    path('inventario/nuevo/', views.crear_equipo, name='crear_equipo'),
    path('inventario/editar/<int:id>/', views.editar_equipo, name='editar_equipo'),
    path('inventario/borrar/<int:id>/', views.borrar_equipo, name='borrar_equipo'),

    # ==========================================
    # 3. MÓDULO CLÍNICO (PROGRAMAS DE SALUD)
    # ==========================================
    
    # Historial General y Panel de Triaje
    path('consultas/', views.lista_consultas, name='lista_consultas'), # Tabla principal con buscador
    path('consultas/seleccionar-programa/', views.seleccionar_programa, name='seleccionar_programa'), # Menú de los 3 botones
    
    # Programa 1: Control Endocrino y Signos Vitales
    path('consultas/endocrino/nuevo/', views.crear_control_endocrino, name='crear_control_endocrino'),
    path('consultas/endocrino/<int:pk>/', views.detalle_control_endocrino, name='detalle_control_endocrino'),
    path('consultas/endocrino/<int:pk>/editar/', views.editar_control_endocrino, name='editar_control_endocrino'),
    path('consultas/endocrino/<int:pk>/eliminar/', views.eliminar_control_endocrino, name='eliminar_control_endocrino'),
    
    # Programa 2: Ruta Materna (Estructura base - Próximamente activa)
    path('consultas/ruta-materna/nuevo/', views.crear_ruta_materna, name='crear_ruta_materna'),
    
    # Programa 3: Planificación Familiar (Estructura base - Próximamente activa)
    path('consultas/planificacion/nuevo/', views.crear_planificacion_familiar, name='crear_planificacion_familiar'),
]
