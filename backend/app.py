# app.py
from flask import Flask
from routes.usuario_routes import usuario_bp
from routes.receta_routes import receta_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.register_blueprint(usuario_bp)
app.register_blueprint(receta_bp)

@app.route("/")
def inicio():
    return "¡Hola, SmartChef está vivo!"

if __name__ == "__main__":
    app.run(debug=True)
