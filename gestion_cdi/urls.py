from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Autenticación
    path('login/', auth_views.LoginView.as_view(template_name='gestion_cdi/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Inicio
    path('', views.inicio, name='inicio'),
    
    # CRUD de Pacientes
    path('pacientes/', views.lista_pacientes, name='lista_pacientes'),
    path('pacientes/nuevo/', views.crear_paciente, name='crear_paciente'),
    path('pacientes/editar/<int:cedula>/', views.editar_paciente, name='editar_paciente'),
    path('pacientes/borrar/<int:cedula>/', views.borrar_paciente, name='borrar_paciente'),

    # CRUD de Personal
    path('personal/', views.lista_personal, name='lista_personal'),
    path('personal/nuevo/', views.crear_personal, name='crear_personal'),
    path('personal/editar/<int:cedula>/', views.editar_personal, name='editar_personal'),
    path('personal/borrar/<int:cedula>/', views.borrar_personal, name='borrar_personal'),

    # CRUD de Inventario de Equipos
    path('inventario/', views.lista_equipos, name='lista_equipos'),
    path('inventario/nuevo/', views.crear_equipo, name='crear_equipo'),
    path('inventario/editar/<int:id>/', views.editar_equipo, name='editar_equipo'),
    path('inventario/borrar/<int:id>/', views.borrar_equipo, name='borrar_equipo'),
]