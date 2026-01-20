from django.urls import path
from . import views

urlpatterns = [
    # 1. Dashboard
    path('', views.dashboard, name='dashboard'),
    path('programas/<str:programa_nombre>/', views.lista_programa, name='lista_programa'),
    
    # 2. Pacientes
    path('pacientes/', views.lista_pacientes, name='pacientes_lista'),
    path('pacientes/crear/', views.crear_paciente, name='crear_paciente'),
    path('pacientes/editar/<int:paciente_id>/', views.editar_paciente, name='editar_paciente'), 
    
    # 3. Consultas e Historia
    path('pacientes/<int:paciente_id>/consulta/', views.registrar_consulta, name='registrar_consulta'),
    path('pacientes/<int:paciente_id>/historia/', views.historia_clinica, name='historia_clinica'),

    # 4. gestion de usuarios 
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/nuevo/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/editar/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    
]