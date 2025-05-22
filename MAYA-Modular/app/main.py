# from flask import Flask
# from app.tablas_busqueda import tablas_bp

# app = Flask(__name__)
# app.register_blueprint(tablas_bp, url_prefix='/tablas')

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8083, debug=True)


from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8083, debug=True)
