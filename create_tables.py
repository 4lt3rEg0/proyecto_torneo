from app import create_app, db
from app.models import Usuario, Juego, Participante, Partida

app = create_app()

with app.app_context():
    # Crear todas las tablas
    db.create_all()

    # Crear usuario administrador por defecto (opcional)
    if not Usuario.query.filter_by(email='admin@torneo.com').first():
        admin = Usuario(
            email='admin@torneo.com',
            nombre='Administrador',
            password='pbkdf2:sha256:260000$TuHashAqui$...',  # Cambiar por hash real
            es_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("Usuario administrador creado: admin@torneo.com")

    print("Base de datos inicializada correctamente!")