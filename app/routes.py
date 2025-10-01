from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user, login_user, logout_user
from .models import db, Usuario, Juego, Participante, Partida
from datetime import datetime, timedelta

main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)


# ===== FUNCIONES AUXILIARES =====
def es_admin():
    return current_user.is_authenticated and current_user.es_admin


# ===== RUTAS DE AUTENTICACIÓN =====
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and usuario.check_password(password):
            login_user(usuario)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.dashboard'))
        else:
            flash('Email o contraseña incorrectos', 'danger')

    return render_template('auth/login.html')


@auth.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        nombre = request.form.get('nombre', '').strip()
        password = request.form.get('password', '')
        confirmar = request.form.get('confirmar', '')

        # Validaciones
        if not all([email, nombre, password]):
            flash('Todos los campos son obligatorios', 'danger')
        elif password != confirmar:
            flash('Las contraseñas no coinciden', 'danger')
        elif len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres', 'danger')
        elif Usuario.query.filter_by(email=email).first():
            flash('El email ya está registrado', 'danger')
        else:
            nuevo_usuario = Usuario(
                email=email,
                nombre=nombre,
                es_admin=False
            )
            nuevo_usuario.set_password(password)

            db.session.add(nuevo_usuario)
            db.session.commit()

            flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('auth.login'))

    return render_template('auth/registro.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('auth.login'))


# ===== RUTAS PRINCIPALES =====
@main.route('/')
def index():
    return redirect(url_for('auth.login'))


@main.route('/dashboard')
@login_required
def dashboard():
    # Obtener juegos activos (simulan torneos)
    juegos = Juego.query.filter_by(activo=True).all()

    # Verificar inscripciones del usuario y obtener niveles
    mis_inscripciones = Participante.query.filter_by(usuario_id=current_user.id).all()
    juegos_inscrito = [insc.juego_id for insc in mis_inscripciones]
    participante_nivel = {insc.juego_id: insc.nivel for insc in mis_inscripciones}

    # Estadísticas básicas
    total_juegos = len(juegos)
    total_inscrito = len(mis_inscripciones)

    # Ranking global (mejores puntuaciones por usuario) - CONSULTA CORREGIDA
    ranking_global = db.session.query(
        Usuario.id.label('usuario_id'),
        Usuario.nombre,
        db.func.max(Partida.puntuacion).label('max_puntuacion'),
        Juego.nombre.label('juego_nombre'),
        Juego.id.label('juego_id'),  # ¡ESTA LÍNEA FALTABA!
        Participante.nivel
    ).join(Participante, Participante.usuario_id == Usuario.id) \
        .join(Partida, Partida.participante_id == Participante.id) \
        .join(Juego, Juego.id == Partida.juego_id) \
        .group_by(Usuario.id, Juego.id) \
        .order_by(db.desc('max_puntuacion')) \
        .limit(10).all()

    # Calcular ranking promedio del usuario
    user_ranking = None
    for i, item in enumerate(ranking_global, 1):
        if item.usuario_id == current_user.id:
            user_ranking = i
            break

    current_year = datetime.now().year

    return render_template('dashboard.html',
                           juegos=juegos,
                           juegos_inscrito=juegos_inscrito,
                           participante_nivel=participante_nivel,
                           total_juegos=total_juegos,
                           total_inscrito=total_inscrito,
                           ranking_global=ranking_global,
                           ranking_promedio=user_ranking,
                           current_year=current_year,
                           timedelta=timedelta)


@main.route('/inscribir/<int:juego_id>', methods=['POST'])
@login_required
def inscribir(juego_id):
    juego = Juego.query.get_or_404(juego_id)

    # Verificar si ya está inscrito
    if Participante.query.filter_by(usuario_id=current_user.id, juego_id=juego_id).first():
        flash('Ya estás inscrito en este juego', 'warning')
        return redirect(url_for('main.dashboard'))

    # Crear nueva inscripción
    nuevo_participante = Participante(
        usuario_id=current_user.id,
        juego_id=juego_id,
        nivel=request.form.get('nivel', 'normal')
    )

    db.session.add(nuevo_participante)
    db.session.commit()

    flash(f'¡Inscripción exitosa en {juego.nombre}!', 'success')
    return redirect(url_for('main.dashboard'))


@main.route('/juego/<int:juego_id>')
@login_required
def detalle_juego(juego_id):
    juego = Juego.query.get_or_404(juego_id)
    participante = Participante.query.filter_by(usuario_id=current_user.id, juego_id=juego_id).first()

    if not participante:
        flash('Debes estar inscrito para ver los detalles del juego', 'warning')
        return redirect(url_for('main.dashboard'))

    # Obtener partidas del usuario en este juego
    mis_partidas = Partida.query.filter_by(participante_id=participante.id) \
        .order_by(Partida.fecha_partida.desc()) \
        .all()

    # Obtener ranking del juego - CONSULTA CORREGIDA
    ranking = db.session.query(
        Usuario.nombre,
        Partida.puntuacion,
        Partida.tiempo,
        Partida.fecha_partida
    ).select_from(Partida) \
        .join(Participante, Partida.participante_id == Participante.id) \
        .join(Usuario, Participante.usuario_id == Usuario.id) \
        .filter(Partida.juego_id == juego_id) \
        .order_by(Partida.puntuacion.desc()) \
        .limit(10) \
        .all()

    return render_template('juego_detalle.html',
                           juego=juego,
                           participante=participante,
                           mis_partidas=mis_partidas,
                           ranking=ranking)


@main.route('/ranking')
@login_required
def ranking_global():
    """Vista del ranking global de todos los torneos"""

    # Obtener top 20 mejores puntuaciones de todos los tiempos
    ranking = db.session.query(
        Usuario.id.label('usuario_id'),
        Usuario.nombre,
        db.func.max(Partida.puntuacion).label('mejor_puntuacion'),
        Juego.nombre.label('juego_nombre'),
        Juego.id.label('juego_id'),
        Participante.nivel,
        db.func.count(Partida.id).label('total_partidas')
    ).join(Participante, Participante.usuario_id == Usuario.id) \
        .join(Partida, Partida.participante_id == Participante.id) \
        .join(Juego, Juego.id == Partida.juego_id) \
        .group_by(Usuario.id, Juego.id) \
        .order_by(db.desc('mejor_puntuacion')) \
        .limit(20).all()

    # Estadísticas adicionales
    total_jugadores = Usuario.query.count()
    total_partidas = Partida.query.count()
    juegos_activos_list = Juego.query.filter_by(activo=True).all()

    return render_template('ranking.html',
                           ranking=ranking,
                           total_jugadores=total_jugadores,
                           total_partidas=total_partidas,
                           juegos_activos=len(juegos_activos_list),
                           juegos_activos_list=juegos_activos_list)


@main.route('/ranking/<int:juego_id>')
@login_required
def ranking_juego(juego_id):
    """Ranking específico de un juego"""
    juego = Juego.query.get_or_404(juego_id)

    ranking = db.session.query(
        Usuario.nombre,
        db.func.max(Partida.puntuacion).label('mejor_puntuacion'),
        db.func.avg(Partida.puntuacion).label('promedio_puntuacion'),
        db.func.count(Partida.id).label('partidas_jugadas'),
        Participante.nivel
    ).join(Participante, Participante.usuario_id == Usuario.id) \
        .join(Partida, Partida.participante_id == Participante.id) \
        .filter(Partida.juego_id == juego_id) \
        .group_by(Usuario.id) \
        .order_by(db.desc('mejor_puntuacion')) \
        .all()

    return render_template('ranking_juego.html',
                           juego=juego,
                           ranking=ranking)


@main.route('/registrar_partida', methods=['POST'])
@login_required
def registrar_partida():
    juego_id = request.form.get('juego_id', type=int)
    puntuacion = request.form.get('puntuacion', type=int)
    tiempo = request.form.get('tiempo', type=float)

    if not all([juego_id, puntuacion is not None, tiempo is not None]):
        flash('Datos incompletos', 'danger')
        return redirect(url_for('main.dashboard'))

    # Verificar inscripción
    participante = Participante.query.filter_by(usuario_id=current_user.id, juego_id=juego_id).first()
    if not participante:
        flash('No estás inscrito en este juego', 'danger')
        return redirect(url_for('main.dashboard'))

    # Registrar partida
    nueva_partida = Partida(
        juego_id=juego_id,
        participante_id=participante.id,
        puntuacion=puntuacion,
        tiempo=tiempo
    )

    db.session.add(nueva_partida)
    db.session.commit()

    flash('Partida registrada correctamente', 'success')
    return redirect(url_for('main.detalle_juego', juego_id=juego_id))


# ===== API PARA GRÁFICAS =====
@main.route('/api/ranking/<int:juego_id>')
@login_required
def api_ranking(juego_id):
    ranking = db.session.query(
        Usuario.nombre,
        Partida.puntuacion,
        Partida.tiempo,
        Partida.fecha_partida
    ).join(Participante).join(Usuario).filter(
        Partida.juego_id == juego_id
    ).order_by(Partida.puntuacion.desc()).limit(15).all()

    data = [{
        'nombre': item.nombre,
        'puntuacion': item.puntuacion,
        'tiempo': item.tiempo,
        'fecha': item.fecha_partida.strftime('%d/%m/%Y %H:%M')
    } for item in ranking]

    return jsonify(data)


@main.route('/api/estadisticas')
@login_required
def api_estadisticas():
    if not es_admin():
        return jsonify({'error': 'No autorizado'}), 403

    # Estadísticas generales para admin
    total_usuarios = Usuario.query.count()
    total_juegos = Juego.query.count()
    total_partidas = Partida.query.count()

    return jsonify({
        'total_usuarios': total_usuarios,
        'total_juegos': total_juegos,
        'total_partidas': total_partidas
    })


# ===== RUTAS DE ADMINISTRADOR =====
@main.route('/admin')
@login_required
def admin_dashboard():
    if not es_admin():
        flash('Acceso denegado. Se requiere permisos de administrador.', 'danger')
        return redirect(url_for('main.dashboard'))

    estadisticas = {
        'usuarios': Usuario.query.count(),
        'juegos': Juego.query.count(),
        'participantes': Participante.query.count(),
        'partidas': Partida.query.count()
    }

    ultimos_usuarios = Usuario.query.order_by(Usuario.fecha_registro.desc()).limit(5).all()
    ultimos_juegos = Juego.query.order_by(Juego.fecha_creacion.desc()).limit(5).all()

    return render_template('admin/dashboard.html',
                           estadisticas=estadisticas,
                           ultimos_usuarios=ultimos_usuarios,
                           ultimos_juegos=ultimos_juegos)


@main.route('/admin/usuarios')
@login_required
def admin_usuarios():
    if not es_admin():
        return redirect(url_for('main.dashboard'))

    usuarios = Usuario.query.order_by(Usuario.fecha_registro.desc()).all()
    return render_template('admin/usuarios.html', usuarios=usuarios)


@main.route('/admin/juegos')
@login_required
def admin_juegos():
    if not es_admin():
        return redirect(url_for('main.dashboard'))

    juegos = Juego.query.order_by(Juego.fecha_creacion.desc()).all()

    # Calcular total de inscripciones
    total_inscripciones = sum(len(juego.participantes) for juego in juegos)

    return render_template('admin/juegos.html',
                           juegos=juegos,
                           total_inscripciones=total_inscripciones)


@main.route('/admin/crear_juego', methods=['POST'])
@login_required
def crear_juego():
    if not es_admin():
        return redirect(url_for('main.dashboard'))

    nombre = request.form.get('nombre', '').strip()
    descripcion = request.form.get('descripcion', '').strip()

    if not nombre:
        flash('El nombre del juego es obligatorio', 'danger')
        return redirect(url_for('main.admin_juegos'))

    nuevo_juego = Juego(nombre=nombre, descripcion=descripcion)
    db.session.add(nuevo_juego)
    db.session.commit()

    flash(f'Juego "{nombre}" creado exitosamente', 'success')
    return redirect(url_for('main.admin_juegos'))


@main.route('/admin/eliminar_juego/<int:juego_id>')
@login_required
def eliminar_juego(juego_id):
    if not es_admin():
        return redirect(url_for('main.dashboard'))

    juego = Juego.query.get_or_404(juego_id)
    db.session.delete(juego)
    db.session.commit()

    flash('Juego eliminado correctamente', 'success')
    return redirect(url_for('main.admin_juegos'))