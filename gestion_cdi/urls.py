from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    #ruta del  login
    path('login/', auth_views.LoginView.as_view(template_name='gestion_cdi/login.html'), name='login'),
    #ruta del logout
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # Ruta para la página de inicio del CDI
    path('', views.inicio, name='inicio'), 

    # Rutas para la gestión de pacientes
    path('pacientes/', views.lista_pacientes, name='lista_pacientes'),
    path('pacientes/nuevo/', views.crear_paciente, name='crear_paciente'),
    path('pacientes/editar/<int:cedula>/', views.editar_paciente, name='editar_paciente'),
    path('pacientes/borrar/<int:cedula>/', views.borrar_paciente, name='borrar_paciente'),

    # Rutas para la gestión de personal del CDI
    path('personal/', views.lista_personal, name='lista_personal'),
    path('personal/nuevo/', views.crear_personal, name='crear_personal'),
    path('personal/editar/<int:cedula>/', views.editar_personal, name='editar_personal'),
    path('personal/borrar/<int:cedula>/', views.borrar_personal, name='borrar_personal'),

]