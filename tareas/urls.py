from django.urls import path
from . import views

# OJO: Debe llamarse 'urlpatterns' (plural) y ser una lista []
urlpatterns = [
    path('', views.lista_tareas, name='lista_tareas'),
]