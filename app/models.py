from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    es_admin = db.Column(db.Boolean, default=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)  # Cambiado a utcnow

    # Relaciones
    participaciones = db.relationship('Participante', backref='usuario', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<Usuario {self.email}>'


class Juego(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)

    # Relaciones
    participantes = db.relationship('Participante', backref='juego', lazy=True, cascade='all, delete-orphan')
    partidas = db.relationship('Partida', backref='juego', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Juego {self.nombre}>'


class Participante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    juego_id = db.Column(db.Integer, db.ForeignKey('juego.id'), nullable=False)
    nivel = db.Column(db.String(20), default='normal')  # amateur, normal, expert
    fecha_inscripcion = db.Column(db.DateTime, default=datetime.utcnow)

    # Relación
    partidas = db.relationship('Partida', backref='participante', lazy=True, cascade='all, delete-orphan')

    # Restricción única para evitar inscripciones duplicadas
    __table_args__ = (db.UniqueConstraint('usuario_id', 'juego_id', name='_usuario_juego_uc'),)

    def __repr__(self):
        return f'<Participante {self.usuario_id} - Juego {self.juego_id}>'


class Partida(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    juego_id = db.Column(db.Integer, db.ForeignKey('juego.id'), nullable=False)
    participante_id = db.Column(db.Integer, db.ForeignKey('participante.id'), nullable=False)
    puntuacion = db.Column(db.Integer, nullable=False)
    tiempo = db.Column(db.Float, nullable=False)  # en segundos
    fecha_partida = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Partida {self.participante_id} - Puntos: {self.puntuacion}>'