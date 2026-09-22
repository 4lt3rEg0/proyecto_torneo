from app import create_app, db
import os

app = create_app()


@app.cli.command("create-db")
def create_db():
    """Crear tablas de la base de datos."""
    with app.app_context():
        db.create_all()
    print("Base de datos creada exitosamente!")


@app.cli.command("seed-db")
def seed_db():
    """Poblar la base de datos con datos de ejemplo."""
    from app.models import Usuario, Juego

    admin_password = os.environ.get("SEED_ADMIN_PASSWORD")
    if not admin_password:
        raise RuntimeError(
            "Define SEED_ADMIN_PASSWORD antes de ejecutar 'flask seed-db'."
        )

    with app.app_context():
        if not Usuario.query.filter_by(email='admin@torneo.com').first():
            admin = Usuario(
                email='admin@torneo.com',
                nombre='Administrador',
                es_admin=True
            )
            admin.set_password(admin_password)
            db.session.add(admin)

        if Juego.query.count() == 0:
            juegos = [
                Juego(nombre='Carrera de Velocidad', descripcion='Completa el circuito en el menor tiempo posible'),
                Juego(nombre='Batalla Espacial', descripcion='Destruye la mayor cantidad de naves enemigas'),
                Juego(nombre='Rompecabezas Extremo', descripcion='Resuelve puzzles contra el reloj')
            ]
            db.session.add_all(juegos)

        db.session.commit()
    print("Datos de ejemplo agregados!")


if __name__ == '__main__':
    app.run(
        debug=os.environ.get("FLASK_DEBUG") == "1",
        host='0.0.0.0',
        port=5000
    )
