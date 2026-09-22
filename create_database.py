import os

from app import create_app, db
from app.models import Usuario, Juego, Participante, Partida


def crear_base_datos():
    admin_password = os.environ.get("SEED_ADMIN_PASSWORD")
    if not admin_password:
        raise RuntimeError("Define SEED_ADMIN_PASSWORD antes de crear los datos de ejemplo.")

    app = create_app()

    with app.app_context():
        db.drop_all()
        db.create_all()

        print("✅ Tablas creadas exitosamente")

        admin = Usuario(
            email='admin@torneo.com',
            nombre='Administrador Principal',
            es_admin=True
        )
        admin.set_password(admin_password)
        db.session.add(admin)

        juegos = [
            Juego(
                nombre='Carrera de Velocidad Extrema',
                descripcion='Completa el circuito en el menor tiempo posible. Evita obstáculos y mejora tu tiempo.'
            ),
            Juego(
                nombre='Batalla Espacial Interestelar',
                descripcion='Destruye la mayor cantidad de naves enemigas. Cada nave vale puntos diferentes.'
            ),
            Juego(
                nombre='Rompecabezas Extremo',
                descripcion='Resuelve puzzles complejos contra el reloj. La velocidad y precisión son clave.'
            ),
            Juego(
                nombre='Supervivencia Zombie',
                descripcion='Sobrevive el mayor tiempo posible contra hordas de zombies. Cada zombie eliminado suma puntos.'
            )
        ]

        db.session.add_all(juegos)
        db.session.commit()

        print("✅ Usuario administrador creado: admin@torneo.com")
        print("✅ Juegos de ejemplo creados:")
        for juego in juegos:
            print(f"   - {juego.nombre}")

        print("\n📊 Estructura de la base de datos:")
        print(f"   Usuarios: {Usuario.query.count()}")
        print(f"   Juegos: {Juego.query.count()}")
        print(f"   Participantes: {Participante.query.count()}")
        print(f"   Partidas: {Partida.query.count()}")


if __name__ == '__main__':
    crear_base_datos()
