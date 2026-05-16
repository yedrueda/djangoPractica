from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'), # Ruta para la página de inicio del CDI
]