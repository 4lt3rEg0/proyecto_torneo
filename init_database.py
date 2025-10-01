import os
import sys
from app import create_app, db
from app.models import Usuario, Juego, Participante, Partida
from datetime import datetime


def init_database():
    """
    Sistema de inicialización de base de datos profesional
    Soporta SQLite, PostgreSQL, MySQL
    """
    app = create_app()

    with app.app_context():
        print("🚀 INICIALIZADOR DE BASE DE DATOS - TORNEO DE VIDEOJUEGOS")
        print("=" * 60)

        # Detectar tipo de base de datos
        db_url = app.config['SQLALCHEMY_DATABASE_URI']
        if 'postgresql' in db_url:
            db_type = "PostgreSQL"
        elif 'mysql' in db_url:
            db_type = "MySQL"
        else:
            db_type = "SQLite"

        print(f"📊 Tipo de Base de Datos: {db_type}")
        print(f"🔗 URL: {db_url}")
        print("-" * 60)

        try:
            # Crear todas las tablas
            print("🔄 Creando tablas...")
            db.create_all()
            print("✅ Tablas creadas exitosamente")

            # Verificar si ya hay datos
            if Usuario.query.count() > 0:
                print("ℹ️  La base de datos ya contiene datos")
                mostrar_estadisticas()
                return

            # Poblar con datos de ejemplo
            print("📥 Insertando datos de ejemplo...")
            poblar_datos_ejemplo()

            print("🎉 Base de datos inicializada correctamente!")
            mostrar_estadisticas()

        except Exception as e:
            print(f"❌ Error durante la inicialización: {e}")
            sys.exit(1)


def poblar_datos_ejemplo():
    """Insertar datos de ejemplo para demostración"""

    # 1. Crear usuario administrador
    admin = Usuario(
        email='admin@torneo.com',
        nombre='Administrador Principal',
        es_admin=True
    )
    admin.set_password('admin123')
    db.session.add(admin)

    # 2. Crear usuario normal de ejemplo
    usuario_ejemplo = Usuario(
        email='jugador@ejemplo.com',
        nombre='Jugador Demo',
        es_admin=False
    )
    usuario_ejemplo.set_password('jugador123')
    db.session.add(usuario_ejemplo)

    # 3. Crear juegos/torneos de ejemplo
    juegos = [
        Juego(
            nombre='Torneo Velocidad Extrema',
            descripcion='Competición contra el reloj: el menor tiempo gana. Modalidad: Carrera contra el tiempo.'
        ),
        Juego(
            nombre='Campeonato de Puntuación',
            descripcion='Acumula la mayor cantidad de puntos. Modalidad: Por acumulación de puntos.'
        ),
        Juego(
            nombre='Liga Supervivencia',
            descripcion='Modo último en pie: sobrevive el mayor tiempo posible. Modalidad: Eliminación.'
        ),
        Juego(
            nombre='Desafío Precisión Máxima',
            descripcion='Cada acierto cuenta. La precisión es clave. Modalidad: Por exactitud.'
        )
    ]

    db.session.add_all(juegos)
    db.session.commit()

    # 4. Crear inscripciones de ejemplo
    from datetime import datetime, timedelta

    # Admin se inscribe en todos los juegos
    for juego in juegos:
        participante = Participante(
            usuario_id=admin.id,
            juego_id=juego.id,
            nivel='expert',
            fecha_inscripcion=datetime.utcnow()
        )
        db.session.add(participante)

    # Usuario demo se inscribe en 2 juegos
    for juego in juegos[:2]:
        participante = Participante(
            usuario_id=usuario_ejemplo.id,
            juego_id=juego.id,
            nivel='normal',
            fecha_inscripcion=datetime.utcnow()
        )
        db.session.add(participante)

    db.session.commit()

    # 5. Crear partidas de ejemplo
    participantes = Participante.query.all()

    for participante in participantes:
        for i in range(3):  # 3 partidas por participante
            partida = Partida(
                juego_id=participante.juego_id,
                participante_id=participante.id,
                puntuacion=500 + (i * 100) + (participante.id * 10),
                tiempo=60.0 + (i * 5) + (participante.id * 0.5),
                fecha_partida=datetime.utcnow() - timedelta(days=3 - i)
            )
            db.session.add(partida)

    db.session.commit()


def mostrar_estadisticas():
    """Mostrar estadísticas de la base de datos"""
    print("\n📊 ESTADÍSTICAS DE LA BASE DE DATOS:")
    print("-" * 40)
    print(f"👤 Usuarios: {Usuario.query.count()}")
    print(f"🎮 Juegos/Torneos: {Juego.query.count()}")
    print(f"📝 Inscripciones: {Participante.query.count()}")
    print(f"🕹️  Partidas registradas: {Partida.query.count()}")

    print("\n🔑 CREDENCIALES DE ACCESO:")
    print("-" * 40)
    print("Administrador: admin@torneo.com / admin123")
    print("Jugador Demo:  jugador@ejemplo.com / jugador123")

    print("\n🎯 INSTRUCCIONES:")
    print("-" * 40)
    print("1. Ejecuta: python run.py")
    print("2. Abre: http://127.0.0.1:5000")
    print("3. Usa las credenciales anteriores")


if __name__ == '__main__':
    init_database()