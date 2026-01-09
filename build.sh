#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Instalar librerías
pip install -r requirements.txt

# 2. Recolectar estáticos (CSS/JS)
python manage.py collectstatic --no-input

# 3. Crear las tablas en la base de datos de la nube
python manage.py migrate

# Crear o actualizar superusuario automáticamente
# Esto usa un comando de Python para no pedir interacción de teclado
python manage.py shell <<EOF
from django.contrib.auth.models import User
username = 'admin'
email = 'yelkindavid1997@gmail.com'
password = 'admin'
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print("Superusuario creado con éxito")
else:
    user = User.objects.get(username=username)
    user.set_password(password)
    user.save()
    print("Password de superusuario actualizado")
EOF