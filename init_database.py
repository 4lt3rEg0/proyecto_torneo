import os
import sys
from datetime import datetime, timedelta

from app import create_app, db
from app.models import Usuario, Juego, Participante, Partida


def init_database():
    """Inicializa la base de datos y carga datos de demostración."""
    app = create_app()

    with app.app_context():
        print("🚀 INICIALIZADOR DE BASE DE DATOS - TORNEO DE VIDEOJUEGOS")
        print("=" * 60)

        db_url = app.config['SQLALCHEMY_DATABASE_URI']
        if 'postgresql' in db_url:
            db_type = "PostgreSQL"
        elif 'mysql' in db_url:
            db_type = "MySQL"
        else:
            db_type = "SQLite"

        print(f"📊 Tipo de Base de Datos: {db_type}")
        print("-" * 60)

        try:
            db.create_all()
            print("✅ Tablas creadas exitosamente")

            if Usuario.query.count() > 0:
                print("ℹ️  La base de datos ya contiene datos")
                mostrar_estadisticas()
                return

            poblar_datos_ejemplo()
            print("🎉 Base de datos inicializada correctamente!")
            mostrar_estadisticas()

        except Exception as e:
            print(f"❌ Error durante la inicialización: {e}")
            sys.exit(1)


def poblar_datos_ejemplo():
    """Insertar datos de ejemplo para demostración."""
    admin_password = os.environ.get("SEED_ADMIN_PASSWORD")
    user_password = os.environ.get("SEED_USER_PASSWORD")

    if not admin_password or not user_password:
        raise RuntimeError(
            "Define SEED_ADMIN_PASSWORD y SEED_USER_PASSWORD antes de inicializar los datos demo."
        )

    admin = Usuario(
        email='admin@torneo.com',
        nombre='Administrador Principal',
        es_admin=True
    )
    admin.set_password(admin_password)
    db.session.add(admin)

    usuario_ejemplo = Usuario(
        email='jugador@ejemplo.com',
        nombre='Jugador Demo',
        es_admin=False
    )
    usuario_ejemplo.set_password(user_password)
    db.session.add(usuario_ejemplo)

    juegos = [
        Juego(
            nombre='Torneo Velocidad Extrema',
            descripcion='Competición contra el reloj: el menor tiempo gana.'
        ),
        Juego(
            nombre='Campeonato de Puntuación',
            descripcion='Acumula la mayor cantidad de puntos.'
        ),
        Juego(
            nombre='Liga Supervivencia',
            descripcion='Modo último en pie: sobrevive el mayor tiempo posible.'
        ),
        Juego(
            nombre='Desafío Precisión Máxima',
            descripcion='Cada acierto cuenta. La precisión es clave.'
        )
    ]

    db.session.add_all(juegos)
    db.session.commit()

    for juego in juegos:
        db.session.add(Participante(
            usuario_id=admin.id,
            juego_id=juego.id,
            nivel='expert',
            fecha_inscripcion=datetime.utcnow()
        ))

    for juego in juegos[:2]:
        db.session.add(Participante(
            usuario_id=usuario_ejemplo.id,
            juego_id=juego.id,
            nivel='normal',
            fecha_inscripcion=datetime.utcnow()
        ))

    db.session.commit()

    participantes = Participante.query.all()
    for participante in participantes:
        for i in range(3):
            db.session.add(Partida(
                juego_id=participante.juego_id,
                participante_id=participante.id,
                puntuacion=500 + (i * 100) + (participante.id * 10),
                tiempo=60.0 + (i * 5) + (participante.id * 0.5),
                fecha_partida=datetime.utcnow() - timedelta(days=3 - i)
            ))

    db.session.commit()


def mostrar_estadisticas():
    print("\n📊 ESTADÍSTICAS DE LA BASE DE DATOS:")
    print("-" * 40)
    print(f"👤 Usuarios: {Usuario.query.count()}")
    print(f"🎮 Juegos/Torneos: {Juego.query.count()}")
    print(f"📝 Inscripciones: {Participante.query.count()}")
    print(f"🕹️  Partidas registradas: {Partida.query.count()}")
    print("\nUsuarios demo: admin@torneo.com y jugador@ejemplo.com")
    print("Las contraseñas se leen de variables de entorno; no se guardan en el repositorio.")


if __name__ == '__main__':
    init_database()
