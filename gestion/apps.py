from django.apps import AppConfig
from django.db.models.signals import post_migrate

def crear_grupos_permisos(sender, **kwargs):
    from django.contrib.auth.models import Group
    Group.objects.get_or_create(name='Administrador')
    Group.objects.get_or_create(name='Médico')
    Group.objects.get_or_create(name='Recepción')
    print("SISTEMA: Grupos de seguridad configurados correctamente.")

class GestionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gestion'

    def ready(self):
        post_migrate.connect(crear_grupos_permisos, sender=self)