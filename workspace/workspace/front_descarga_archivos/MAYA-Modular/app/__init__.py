from flask import Flask, redirect
from app.tablas_busqueda import tablas_bp

def create_app():
    app = Flask(__name__)

    # Registrar el blueprint con el prefijo /tablas
    app.register_blueprint(tablas_bp, url_prefix='/tablas')

    # Ruta raíz que redirige a /tablas/
    @app.route('/')
    def index():
        return redirect('/tablas/')

    return app
