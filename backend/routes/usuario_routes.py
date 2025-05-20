# routes/usuario_routes.py

from flask import Blueprint, request, jsonify
from config.database import SessionLocal
from models.user import Usuario
import sqlalchemy.exc

usuario_bp = Blueprint("usuario", __name__)

@usuario_bp.route("/register", methods=["POST"])
def registrar_usuario():
    data = request.json

    nombre = data.get("nombre")
    correo = data.get("correo")
    contraseña = data.get("contraseña")

    if not nombre or not correo or not contraseña:
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    db = SessionLocal()
    try:
        nuevo_usuario = Usuario(nombre=nombre, correo=correo)
        nuevo_usuario.set_contraseña(contraseña)

        db.add(nuevo_usuario)
        db.commit()
        return jsonify({"mensaje": "Usuario registrado correctamente"}), 201
    except sqlalchemy.exc.IntegrityError:
        db.rollback()
        return jsonify({"error": "El correo ya está registrado"}), 400
    finally:
        db.close()

@usuario_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    correo = data.get("correo")
    contraseña = data.get("contraseña")

    if not correo or not contraseña:
        return jsonify({"error": "Correo y contraseña son obligatorios"}), 400

    db = SessionLocal()
    try:
        usuario = db.query(Usuario).filter_by(correo=correo).first()
        if usuario and usuario.verificar_contraseña(contraseña):
            return jsonify({"mensaje": "Inicio de sesión exitoso"})
        else:
            return jsonify({"error": "Credenciales incorrectas"}), 401
    finally:
        db.close()

@usuario_bp.route("/user", methods=["GET"])
def listar_usuarios():
    db = SessionLocal()
    try:
        usuarios = db.query(Usuario).all()
        resultado = []
        for u in usuarios:
            resultado.append({
                "id": u.id,
                "nombre": u.nombre,
                "correo": u.correo
                # No mostramos la contraseña
            })
        return jsonify(resultado)
    finally:
        db.close()
