#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Instalar librerías
pip install -r requirements.txt

# 2. Recolectar estáticos (CSS/JS)
python manage.py collectstatic --no-input

# 3. Crear las tablas en la base de datos de la nube
python manage.py migrate