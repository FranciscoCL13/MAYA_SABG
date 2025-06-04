from flask import Flask, redirect
import secrets

from app.api_adjuntos.routes import api_bp as adjuntos_bp
from app.api_efirma.routes import efirma_bp
from app.api_tablas.tablas_busqueda import tablas_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = secrets.token_hex(32)

    app.register_blueprint(adjuntos_bp)
    app.register_blueprint(efirma_bp)
    app.register_blueprint(tablas_bp, url_prefix='/tablas')

    @app.route('/')
    def index():
        return redirect('/')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=8080)
