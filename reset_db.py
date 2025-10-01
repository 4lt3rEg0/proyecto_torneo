import os
from app import create_app, db
from app.models import Usuario, Juego, Participante, Partida
from datetime import datetime


def reset_database():
    app = create_app()

    with app.app_context():
        # Eliminar archivo de base de datos si existe
        if os.path.exists('torneo.db'):
            os.remove('torneo.db')
            print("🗑️  Base de datos anterior eliminada")

        # Crear nuevas tablas
        db.create_all()
        print("✅ Nueva base de datos creada")

        # Poblar con datos de ejemplo
        from app.models import Usuario, Juego

        # Verificar si el admin ya existe
        admin_existente = Usuario.query.filter_by(email='admin@torneo.com').first()
        if not admin_existente:
            admin = Usuario(
                email='admin@torneo.com',
                nombre='Administrador Principal',
                es_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            print("✅ Usuario administrador creado")
        else:
            print("ℹ️  Usuario administrador ya existe")

        # Verificar si ya hay juegos
        if Juego.query.count() == 0:
            juegos = [
                Juego(
                    nombre='Torneo Velocidad Extrema',
                    descripcion='Competición por tiempo: completa el circuito en el menor tiempo posible. ¡Cada milisegundo cuenta!'
                ),
                Juego(
                    nombre='Campeonato de Puntuación',
                    descripcion='Torneo por puntos: consigue la mayor puntuación posible. Estrategia y precisión son clave.'
                ),
                Juego(
                    nombre='Liga Supervivencia',
                    descripcion='Torneo de eliminación: sobrevive el mayor tiempo posible. ¡El último en pie gana!'
                ),
                Juego(
                    nombre='Desafío Precisión Máxima',
                    descripcion='Competencia de precisión: cada acierto suma puntos. La exactitud es fundamental.'
                )
            ]

            db.session.add_all(juegos)
            print("✅ 4 juegos de ejemplo creados")
        else:
            print("ℹ️  Juegos ya existen en la base de datos")

        try:
            db.session.commit()
            print("✅ Datos de ejemplo agregados exitosamente")

            # Mostrar estadísticas finales
            print(f"\n📊 Estadísticas de la base de datos:")
            print(f"   👤 Usuarios: {Usuario.query.count()}")
            print(f"   🎮 Juegos: {Juego.query.count()}")
            print(f"   📝 Participantes: {Participante.query.count()}")
            print(f"   🕹️  Partidas: {Partida.query.count()}")

            print("\n🔑 Credenciales de acceso:")
            print("   Administrador: admin@torneo.com / admin123")
            print("\n🎯 Puedes registrar nuevos usuarios desde la aplicación")

        except Exception as e:
            db.session.rollback()
            print(f"❌ Error al agregar datos: {e}")


if __name__ == '__main__':
    reset_database()