from flask import Blueprint, request, jsonify, render_template
import requests
import base64
from app.config import Config
from .ocsp_proxy import validar_ocsp

efirma_blueprint = Blueprint('efirma', __name__, template_folder='templates')

KIE_SERVER_URL = Config.KIE_SERVER_URL
KIE_USERNAME = Config.KIE_USERNAME
KIE_PASSWORD = Config.KIE_PASSWORD

@efirma_blueprint.route('/')
def index():
    return render_template('index.html')

@efirma_blueprint.route('/form7')
def form7():
    return render_template('form7.html')

@efirma_blueprint.route('/validar_ocsp', methods=['POST'])
def validar_firma():
    try:
        data = request.get_json(force=True)
        certificado = data.get('certificado')
        if not certificado:
            return jsonify({"error": "Falta el certificado para validar"}), 400

        resultado = validar_ocsp(certificado)

        return jsonify({"resultado": resultado}), 200

    except Exception as e:
        return jsonify({"error": "Error en la validación OCSP", "detalle": str(e)}), 500

@efirma_blueprint.route('/procesar_firma', methods=['POST'])
def procesar_firma():
    try:
        data = request.get_json(force=True)
        documento_id = data.get("documentId")
        firma_digital = data.get("firmaDigital")

        if not documento_id or not firma_digital:
            return jsonify({"error": "Faltan datos para procesar la firma"}), 400

        # Aquí puede integrarse con jBPM o backend para almacenar firma

        return jsonify({"mensaje": f"Firma digital procesada para documento {documento_id}"}), 200

    except Exception as e:
        return jsonify({"error": "Error al procesar la firma", "detalle": str(e)}), 500
