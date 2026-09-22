# Torneo de Videojuegos — Flask

Aplicación web para gestionar torneos de videojuegos, participantes, partidas, puntuaciones y rankings.

## Funcionalidades

- Registro e inicio de sesión.
- Gestión de juegos y participantes.
- Registro de partidas y puntuaciones.
- Ranking y gráficas.
- Panel de administración.
- Interfaz responsive con Bootstrap.

## Tecnologías

- Python / Flask
- Flask-SQLAlchemy
- Flask-Login
- SQLite
- Bootstrap 5
- Chart.js
- Jinja2

## Instalación

```bash
python -m venv .venv
pip install -r requirements.txt
```

Crea la base de datos:

```bash
flask --app run create-db
```

Para cargar datos de demostración, define una contraseña local para el administrador.

PowerShell:

```powershell
$env:SEED_ADMIN_PASSWORD = "elige-una-clave-local"
flask --app run seed-db
```

Bash:

```bash
export SEED_ADMIN_PASSWORD="elige-una-clave-local"
flask --app run seed-db
```

Ejecuta:

```bash
python run.py
```

Para un despliegue real también debe definirse `SECRET_KEY`. El repositorio no contiene claves, contraseñas ni bases de datos locales.

## Estructura

```text
app/
  templates/
  static/
  __init__.py
  models.py
  routes.py
run.py
requirements.txt
```

## Nota

Proyecto académico centrado en autenticación, modelado relacional, CRUD, rankings y visualización de datos.
