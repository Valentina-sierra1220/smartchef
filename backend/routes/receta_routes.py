# routes/receta_routes.py

from flask import Blueprint, request, jsonify
from config.database import SessionLocal
from models.receta import Receta
from models.user import Usuario
from models.receta_guardada import RecetaGuardada

receta_bp = Blueprint("recetas", __name__)


@receta_bp.route("/recetas", methods=["POST"])
def crear_receta():
    data = request.json

    nombre = data.get("nombre")
    descripcion = data.get("descripcion")
    instrucciones = data.get("instrucciones")
    tiempo = data.get("tiempo")
    porciones = data.get("porciones")
    publica = data.get("publica", False)
    id_usuario = data.get("id_usuario")  # simula el usuario actual

    if not all([nombre, instrucciones, id_usuario]):
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    db = SessionLocal()
    try:
        receta = Receta(
            nombre=nombre,
            descripcion=descripcion,
            instrucciones=instrucciones,
            tiempo=tiempo,
            porciones=porciones,
            publica=publica,
            id_usuario=id_usuario
        )
        db.add(receta)
        db.commit()
        return jsonify({"mensaje": "Receta creada correctamente"})
    finally:
        db.close()


@receta_bp.route("/mis-recetas", methods=["GET"])
def recetas_personales():
    id_usuario = request.args.get("id_usuario")

    db = SessionLocal()
    try:
        recetas = db.query(Receta).filter_by(id_usuario=id_usuario).all()
        resultado = []
        for r in recetas:
            resultado.append({
                "id": r.id,
                "nombre": r.nombre,
                "descripcion": r.descripcion,
                "publica": r.publica
            })
        return jsonify(resultado)
    finally:
        db.close()

@receta_bp.route("/feed", methods=["GET"])
def feed_publico():
    db = SessionLocal()
    try:
        recetas = db.query(Receta).filter_by(publica=True).order_by(Receta.fecha_creacion.desc()).all()
        resultado = []
        for r in recetas:
            resultado.append({
                "id": r.id,
                "nombre": r.nombre,
                "descripcion": r.descripcion,
                "tiempo": r.tiempo,
                "publica": r.publica
            })
        return jsonify(resultado)
    finally:
        db.close()


@receta_bp.route("/recetas/<int:id_receta>/guardar", methods=["POST"])
def guardar_receta(id_receta):
    data = request.json
    id_usuario = data.get("id_usuario")

    db = SessionLocal()
    try:
        receta = db.query(Receta).filter_by(id=id_receta, publica=True).first()

        if not receta:
            return jsonify({"error": "La receta no existe o no es pública"}), 404

        if receta.id_usuario == int(id_usuario):
            return jsonify({"error": "No puedes guardar tu propia receta"}), 400

        ya_guardada = db.query(RecetaGuardada).filter_by(id_usuario=id_usuario, id_receta=id_receta).first()
        if ya_guardada:
            return jsonify({"error": "Ya guardaste esta receta"}), 400

        guardada = RecetaGuardada(id_usuario=id_usuario, id_receta=id_receta)
        db.add(guardada)
        db.commit()

        return jsonify({"mensaje": "Receta guardada correctamente"})
    finally:
        db.close()


@receta_bp.route("/guardadas", methods=["GET"])
def recetas_guardadas():
    id_usuario = request.args.get("id_usuario")

    db = SessionLocal()
    try:
        guardadas = db.query(RecetaGuardada).filter_by(id_usuario=id_usuario).all()
        resultado = []

        for g in guardadas:
            receta = db.query(Receta).filter_by(id=g.id_receta).first()
            if receta:
                resultado.append({
                    "id": receta.id,
                    "nombre": receta.nombre,
                    "descripcion": receta.descripcion
                })

        return jsonify(resultado)
    finally:
        db.close()

