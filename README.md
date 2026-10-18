# 🏥 SIGE - CDI "El Llanito"
### Sistema Integral de Gestión para el Centro de Diagnóstico Integral "El Llanito"
**Municipio Sucre, Estado Miranda — Venezuela**

Sistema web desarrollado con **Python** y **Django 6** para la administración clínica, logística y de talento humano del CDI "El Llanito". Permite gestionar pacientes, personal de salud, control de inventario médico y programas de salud comunitaria (Control Endocrino, Ruta Materna y Planificación Familiar).

---

## 📋 Tabla de Contenidos
1. [Requisitos Previos](#-requisitos-previos)
2. [Instalación y Activación](#-instalación-y-activación)
   - [Opción A: Instalación Online](#opción-a-instalación-estándar-con-internet)
   - [Opción B: Instalación Offline (Sin Internet)](#opción-b-instalación-offline-sin-conexión)
3. [Configuración de Base de Datos (Supabase)](#-configuración-de-base-de-datos)
4. [Ejecución del Servidor](#-ejecución-del-servidor)
5. [Acceso al Sistema y Credenciales](#-acceso-al-sistema-y-credenciales)
6. [Módulos Principales](#-módulos-del-sistema)
7. [Comandos de Mantenimiento Útiles](#-comandos-útiles-de-django)

---

## 💻 Requisitos Previos

- **Python 3.10 o superior** (probado y optimizado en Python 3.14).
- **Git** instalado.
- Conexión a internet (para sincronización con Supabase PostgreSQL) o conexión local.

---

## 🚀 Instalación y Activación

### 1. Ubicarse en el directorio del proyecto
Abre una terminal y dirígete a la carpeta raíz del proyecto:
```bash
cd /home/yd/Proyectos/djangoPractica
```

### 2. Activar el Entorno Virtual (`env`)
El proyecto ya cuenta con un entorno virtual configurado en la carpeta `env/`:

**En Linux / macOS:**
```bash
source env/bin/activate
```

*(Si por alguna razón necesitas crearlo desde cero: `python3 -m venv env && source env/bin/activate`)*

**En Windows:**
```powershell
.\env\Scripts\activate
```

Al activarse, verás `(env)` al inicio de tu línea de comandos.

---

### 3. Instalación de Dependencias

#### Opción A: Instalación estándar (con internet)
```bash
pip install -r requirements.txt
```

#### Opción B: Instalación Offline (Sin conexión)
Si estás en una máquina hospitalaria sin acceso a internet, este proyecto incluye las ruedas de instalación (`.whl`) en la carpeta `librerias_offline/`:
```bash
pip install --no-index --find-links=librerias_offline/ -r requirements.txt
```

---

## 🗄️ Configuración de Base de Datos

El sistema está configurado para operar con **Supabase PostgreSQL** mediante un **Connection Pooler** en el puerto `5432` con soporte para redes IPv4 e IPv6.

### Variables de Entorno (Opcional)
Por defecto, el archivo `config/settings.py` ya incluye la cadena de conexión de Supabase. Si deseas sobreescribirla en producción o localmente:
```bash
export DATABASE_URL=
```

### Aplicar Migraciones
Para asegurar que todas las tablas y columnas (incluyendo `carnet_de_la_patria`) estén sincronizadas:
```bash
python manage.py migrate
```

---

## 🌐 Ejecución del Servidor

Con el entorno virtual activo, inicia el servidor de desarrollo:

```bash
python manage.py runserver
```

Para permitir el acceso desde otros dispositivos en la misma red local (WiFi o LAN del CDI):
```bash
python manage.py runserver 0.0.0.0:8000
```

---

## 🔑 Acceso al Sistema y Credenciales

Una vez que el servidor esté corriendo, abre tu navegador web preferido (Chrome, Firefox, Edge):

### 1. Portal Principal y Triaje Virtual
- **URL de Acceso:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/) o [http://localhost:8000/](http://localhost:8000/)
- **Página de Login:** [http://127.0.0.1:8000/login/](http://127.0.0.1:8000/login/)

### 2. Panel Administrativo de Django
- **URL del Panel Admin:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

### 3. Credenciales de Acceso Inicial
- **Usuario Administrador:** `admin`
- **Correo Electrónico:** `yelkindavid1997@gmail.com`
- **Contraseña:** *(Tu contraseña establecida para la cuenta admin)*

> [!TIP]
> **¿Olvidaste o quieres crear un nuevo superusuario?**  
> Puedes crear uno nuevo en cualquier momento ejecutando:
> ```bash
> python manage.py createsuperuser
> ```

---

## 🏥 Módulos del Sistema

| Módulo | Ruta URL | Descripción |
| :--- | :--- | :--- |
| **Inicio / Dashboard** | `/` | Resumen cuantitativo de pacientes, personal, equipos y consultas. |
| **Directorio de Personal** | `/personal/` | Gestión de talento humano (Médicos, Enfermeros, etc.) con indicador de **Carnet de la Patria**. |
| **Turnos de Guardia** | `/guardias/` | Planificación y asignación de guardias médicas/asistenciales, horarios, áreas y suplencias. |
| **Censo y Demografía** | `/poblacion/` | Censo demográfico del ASIC: 8 Comunas, 24 Consultorios Populares (CPT), familias y desglose por género (M/F). |
| **Gestión de Pacientes** | `/pacientes/` | Censo demográfico, control por ASIC y cálculo dinámico de edad. |
| **Inventario de Equipos** | `/inventario/` | Control de Bienes Nacionales (médicos, electrónicos, mobiliario) y estado físico. |
| **Sala de Triaje Clínico** | `/consultas/seleccionar-programa/` | Acceso rápido a los 3 programas de atención comunitaria. |
| **Control Endocrino** | `/consultas/` | Historial médico, signos vitales, analíticas de laboratorio y patologías crónicas. |
| **Ruta Materna** | `/consultas/ruta-materna/nuevo/` | Ficha de control gestacional y semanas de embarazo. |
| **Planificación Familiar** | `/consultas/planificacion/nuevo/` | Control operativo y entrega de métodos anticonceptivos. |

---

## 🛠️ Comandos Útiles de Django

- **Verificar estado de salud del proyecto:**
  ```bash
  python manage.py check
  ```
- **Crear nuevas migraciones si modificas modelos:**
  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```
- **Recolectar archivos estáticos para producción:**
  ```bash
  python manage.py collectstatic
  ```
- **Iniciar shell interactivo de Django:**
  ```bash
  python manage.py shell
  ```
