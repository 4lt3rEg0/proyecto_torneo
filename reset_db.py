import os

from app import create_app, db
from app.models import Usuario, Juego, Participante, Partida


def reset_database():
    admin_password = os.environ.get("SEED_ADMIN_PASSWORD")
    if not admin_password:
        raise RuntimeError("Define SEED_ADMIN_PASSWORD antes de resetear la base de datos.")

    app = create_app()

    with app.app_context():
        db.drop_all()
        db.create_all()
        print("✅ Nueva base de datos creada")

        admin = Usuario(
            email='admin@torneo.com',
            nombre='Administrador Principal',
            es_admin=True
        )
        admin.set_password(admin_password)
        db.session.add(admin)

        juegos = [
            Juego(
                nombre='Torneo Velocidad Extrema',
                descripcion='Competición por tiempo: completa el circuito en el menor tiempo posible.'
            ),
            Juego(
                nombre='Campeonato de Puntuación',
                descripcion='Torneo por puntos: consigue la mayor puntuación posible.'
            ),
            Juego(
                nombre='Liga Supervivencia',
                descripcion='Torneo de eliminación: sobrevive el mayor tiempo posible.'
            ),
            Juego(
                nombre='Desafío Precisión Máxima',
                descripcion='Competencia de precisión: cada acierto suma puntos.'
            )
        ]

        db.session.add_all(juegos)
        db.session.commit()

        print("✅ Datos de ejemplo agregados exitosamente")
        print(f"   👤 Usuarios: {Usuario.query.count()}")
        print(f"   🎮 Juegos: {Juego.query.count()}")
        print(f"   📝 Participantes: {Participante.query.count()}")
        print(f"   🕹️  Partidas: {Partida.query.count()}")
        print("\nAdministrador demo: admin@torneo.com")
        print("La contraseña se toma de SEED_ADMIN_PASSWORD.")


if __name__ == '__main__':
    reset_database()
