from flask import Flask

# Importa aquí los Blueprints para registrarlos luego
from app.api_adjuntos import api_adjuntos_bp
from app.api_efirma import efirma_bp as api_efirma_bp

from app.api_tablas import api_tablas_bp

def create_app():
    app = Flask(__name__)

    # Aquí podrías cargar configuración si tienes, por ejemplo:
    # app.config.from_pyfile('config.py')

    # Registrar los Blueprints
        app.register_blueprint(api_adjuntos_bp, url_prefix="/adjuntos")
        app.register_blueprint(api_efirma_bp, url_prefix="/efirma")
        app.register_blueprint(api_tablas_bp, url_prefix="/tablas")

    return app



