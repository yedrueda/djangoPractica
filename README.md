# 🚀 Sistema de Gestión (Práctica Django + Postgres)

Este es un proyecto de práctica para aprender desarrollo backend con **Django**, conectado a una base de datos **PostgreSQL** corriendo en **Docker**.

## 📋 Requisitos Previos

* **Fedora Linux** (o cualquier distro basada en Linux).
* **Docker** instalado y corriendo.
* **Python 3** y `pip`.

---

## 🛠️ Guía de Inicio Rápido

Sigue estos pasos en orden para levantar el proyecto en tu máquina local.

### 1. Encender la Base de Datos (Docker) 🐳
El proyecto necesita que PostgreSQL esté corriendo en el puerto `5432`.

```bash
# Iniciar el contenedor (si ya existe)
docker start mi_postgres

# O crear uno nuevo si no existe:
# docker run --name mi_postgres -e POSTGRES_PASSWORD=mi_clave_secreta -p 5432:5432 -d postgres

# Activar el Entorno Virtual 🐍

source env/bin/activate

# Ejecutar Migraciones (Solo si hay cambios en DB) 🗂️

python manage.py migrate

# Encender el Servidor 🚀

python manage.py runserver

# El sitio estará disponible en: http://127.0.0.1:8000

# 🔐 Credenciales de Desarrollo


Servicio,Usuario,Contraseña (Dev)
Django Admin,yd (o tu usuario),(La que configuraste)
PostgreSQL,postgres,mi_clave_secreta (postgres)