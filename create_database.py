from app import create_app, db
from app.models import Usuario, Juego, Participante, Partida
from datetime import datetime


def crear_base_datos():
    app = create_app()

    with app.app_context():
        # Eliminar y crear todas las tablas
        db.drop_all()
        db.create_all()

        print("✅ Tablas creadas exitosamente")

        # Crear usuario administrador
        admin = Usuario(
            email='admin@torneo.com',
            nombre='Administrador Principal',
            es_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)

        # Crear juegos de ejemplo
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

        print("✅ Usuario administrador creado:")
        print("   Email: admin@torneo.com")
        print("   Contraseña: admin123")

        print("✅ Juegos de ejemplo creados:")
        for juego in juegos:
            print(f"   - {juego.nombre}")

        # Verificar la estructura de las tablas
        print("\n📊 Estructura de la base de datos:")
        print(f"   Usuarios: {Usuario.query.count()}")
        print(f"   Juegos: {Juego.query.count()}")
        print(f"   Participantes: {Participante.query.count()}")
        print(f"   Partidas: {Partida.query.count()}")


if __name__ == '__main__':
    crear_base_datos()