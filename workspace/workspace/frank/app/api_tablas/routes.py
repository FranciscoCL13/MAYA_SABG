from flask import Blueprint, render_template, request, jsonify
from app.api_tablas.conexion import obtener_documentos
import os

tablas_blueprint = Blueprint('tablas', __name__, template_folder='templates')

@tablas_blueprint.route('/', methods=['GET'])
def index():
    documentos = obtener_documentos()
    return render_template('index.html', documentos=documentos)

@tablas_blueprint.route('/documentos', methods=['GET'])
def lista_documentos():
    documentos = obtener_documentos()
    return jsonify(documentos)
