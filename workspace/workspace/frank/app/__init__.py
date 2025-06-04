from flask import Flask
from app.api_tablas.routes import tablas_blueprint
from app.api_documentos.routes import documentos_blueprint
from app.api_efirma.routes import efirma_blueprint


def create_app():
    app = Flask(__name__)

    # Registro de Blueprints
    app.register_blueprint(tablas_blueprint, url_prefix='/tablas')
    app.register_blueprint(documentos_blueprint, url_prefix='/documentos')
    app.register_blueprint(efirma_blueprint, url_prefix='/efirma')

    return app
