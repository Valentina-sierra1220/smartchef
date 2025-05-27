#routes/receta_routes.py

import os
import json
from flask import current_app
from flask import send_from_directory
from werkzeug.utils import secure_filename
from flask import Blueprint, request, jsonify
from config.database import SessionLocal
from models.receta import Receta
#from models.user import Usuario
from models.receta_guardada import RecetaGuardada
from models.imagen_receta import ImagenReceta

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
        db.refresh(receta)  # 🔄 importante para obtener el id recién generado

        return jsonify({
            "mensaje": "Receta creada correctamente",
            "id_receta": receta.id
        }), 201
    finally:
        db.close()

@receta_bp.route("/recetas/<int:id_receta>", methods=["PUT"])
def actualizar_receta(id_receta):
    data = request.json

    db = SessionLocal()
    try:
        receta = db.query(Receta).filter_by(id=id_receta).first()

        if not receta:
            return jsonify({"error": "Receta no encontrada"}), 404

        # Actualizar campos si vienen en el payload
        receta.nombre = data.get("nombre", receta.nombre)
        receta.descripcion = data.get("descripcion", receta.descripcion)
        receta.instrucciones = data.get("instrucciones", receta.instrucciones)
        receta.tiempo = data.get("tiempo", receta.tiempo)
        receta.porciones = data.get("porciones", receta.porciones)
        receta.publica = data.get("publica", receta.publica)

        db.commit()
        return jsonify({"mensaje": "Receta actualizada correctamente"})
    except Exception as e:
        db.rollback()
        return jsonify({"error": f"Error al actualizar receta: {str(e)}"}), 500
    finally:
        db.close()


@receta_bp.route("/mis-recetas", methods=["GET"])
def recetas_personales():
    id_usuario = request.args.get("id_usuario")

    if not id_usuario:
        return jsonify({"error": "Falta el id_usuario"}), 400

    db = SessionLocal()
    try:
        recetas = (
            db.query(Receta)
            .filter_by(id_usuario=id_usuario)
            .order_by(Receta.id.desc())  # O usa .fecha_creacion.desc() si la tienes
            .limit(20)
            .all()
        )

        resultado = []
        for receta in recetas:
            imagenes = db.query(ImagenReceta).filter_by(id_receta=receta.id).all()
            resultado.append({
                "id": receta.id,
                "nombre": receta.nombre,
                "descripcion": receta.descripcion,
                "instrucciones": receta.instrucciones,
                "tiempo": receta.tiempo,
                "porciones": receta.porciones,
                "publica": receta.publica,
                "id_usuario": receta.id_usuario,
                "imagenes": [img.url for img in imagenes]
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



@receta_bp.route('/imagenes', methods=['GET'])
def obtener_imagenes():
    """
    Devuelve la lista de URLs de imágenes guardadas en static/imagenes.json
    """
    ruta_json = os.path.join(current_app.root_path, 'static', 'imagenes.json')

    try:
        with open(ruta_json, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        datos = []

    return jsonify({'imagenes': datos})


# Carpeta de destino para las imágenes
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@receta_bp.route('/upload', methods=['POST'])
def subir_imagenes():
    upload_folder = os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads')
    upload_folder = os.path.abspath(upload_folder)

    if 'imagenes' not in request.files:
        return jsonify({'error': 'No se encontró ninguna imagen'}), 400

    files = request.files.getlist('imagenes')
    urls = []

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(upload_folder, filename)

            counter = 1
            base, ext = os.path.splitext(filename)
            while os.path.exists(save_path):
                filename = f"{base}_{counter}{ext}"
                save_path = os.path.join(upload_folder, filename)
                counter += 1

            file.save(save_path)

            # Devuelve la ruta accesible por el frontend
            url = f'/static/uploads/{filename}'
            urls.append(url)

    return jsonify({'urls': urls}), 200

@receta_bp.route('/imagenes-receta', methods=['POST'])
def guardar_imagenes_receta():
    data = request.json
    id_receta = data.get('id_receta')
    urls = data.get('urls', [])

    if not id_receta or not urls:
        return jsonify({'error': 'Se requieren id_receta y lista de urls'}), 400

    db = SessionLocal()
    try:
        for url in urls:
            imagen = ImagenReceta(url=url, id_receta=id_receta)
            db.add(imagen)
        db.commit()
        return jsonify({'mensaje': 'Imágenes guardadas correctamente'}), 201
    finally:
        db.close()


