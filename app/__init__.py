from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
import secrets

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    # Use an explicit secret in deployed environments. For local development,
    # generate a temporary secret instead of hardcoding one in source control.
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or secrets.token_hex(32)

    # Configuración de Base de Datos desde variables de entorno
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        # Para PostgreSQL, MySQL, etc.
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        # SQLite por defecto (desarrollo)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///torneo.db'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_recycle': 300,
        'pool_pre_ping': True
    }

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'

    from .models import Usuario

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    from .routes import main, auth
    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')

    return app
