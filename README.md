# Torneo de Videojuegos - Aplicación Web

Aplicación web desarrollada en Python/Flask para la gestión de torneos de videojuegos.

## Características

-  Sistema de autenticación de usuarios
-  Gestión de juegos y participantes
-  Registro de partidas y puntuaciones
-  Ranking en tiempo real con gráficas
-  Panel de administración completo
-  Diseño responsive con Bootstrap 5
-  Gráficas interactivas con Chart.js

## Instalación

1. Clonar el repositorio
2. Crear entorno virtual: `python -m venv venv`
3. Activar entorno: `venv\Scripts\activate` (Windows)
4. Instalar dependencias: `pip install -r requirements.txt`
5. Crear base de datos: `flask create-db`
6. Poblar con datos de ejemplo: `flask seed-db`
7. Ejecutar: `python run.py`

## Estructura del Proyecto

proyecto_torneo/
├── app/
│ ├── templates/ # Templates HTML
│ ├── static/ # CSS, JS, imágenes
│ ├── init.py # Factory de la app
│ ├── models.py # Modelos de datos
│ └── routes.py # Rutas de la aplicación
├── requirements.txt # Dependencias
└── run.py # Punto de entrada


## Usuarios de Prueba

- **Admin:** admin@torneo.com / admin123
- **Usuario normal:** (crear mediante registro)

## Tecnologías Utilizadas

- **Backend:** Flask, SQLAlchemy, Flask-Login
- **Frontend:** Bootstrap 5, Chart.js, Jinja2
- **Base de datos:** SQLite (desarrollo)
- **Iconos:** Bootstrap Icons