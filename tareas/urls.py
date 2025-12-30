from django.urls import path
from . import views

# OJO: Debe llamarse 'urlpatterns' (plural) y ser una lista []
urlpatterns = [
    path('', views.lista_tareas, name='lista_tareas'),
    path('crear/', views.crear_tarea, name='crear_tarea'),
    path('eliminar/<int:tarea_id>/', views.eliminar_tarea, name='eliminar_tarea'),
    path('completar/<int:tarea_id>/', views.completar_tarea, name='completar_tarea'),
]