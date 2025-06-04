from flask import Flask, request, render_template, send_from_directory, url_for, session, redirect, jsonify, Blueprint
import requests
import base64
import uuid
import time
import os
import secrets
# from pycfdi_credentials import Certificate
 
from satcfdi.certifica import Certificate

# from satcfdi import Certificate

# from ocsp_proxy import validar_ocsp_proxy
from .ocsp_proxy import validar_ocsp_proxy

efirma_bp = Blueprint('efirma_bp', __name__)

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)


# === Configuración de carpetas y jBPM ===
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploaded_docs')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

KIE_SERVER_URL = "http://172.25.30.98:8080/kie-server/services/rest/server"
KIE_USERNAME = "wbadmin"
KIE_PASSWORD = "wbadmin"

CONFIG_PROCESOS = {
    "Público": {
        "containerId": "Publica_In_Out_1.0.0-SNAPSHOT",
        "processId": "Publica_In_Out.Publica"
    },
    "Privado": {
        "containerId": "Privada_1.0.0-SNAPSHOT",
        "processId": "Privada.Privada_In_Out"
    },
    "Social": {
        "containerId": "Social_In_Out_1.0.0-SNAPSHOT",
        "processId": "Social_In_Out.Social"
    }
}

# === Rutas ===

@efirma_bp.route("/", methods=['GET'])
def mostrar_index():
    return render_template("form7.html")  # Login con e.firma

@efirma_bp.route("/login", methods=['GET'])
def login_page():
    return render_template("index.html")

@efirma_bp.route("/login", methods=['POST'])
def login():
    data = request.get_json()

    if data and data.get("salir"):
        session.clear()

    elif 'rfc' not in session and 'challenge' in session and all(k in data for k in ['certificado', 'firma_cadena', 'timestamp']) and abs(time.time() - int(data['timestamp'])) <= 300:
        try:
            cert = Certificate(base64.b64decode(data['certificado']))
            if cert.verify(base64.b64decode(data['firma_cadena']), (f"{data['timestamp']}_{session['challenge']}").encode("utf-8"), "sha256"):
                ocsp_result = validar_ocsp_proxy(cert.to_pem().decode())

                if ocsp_result.get("resultado") == "VALIDO":
                    session['rfc'] = cert.subject.rfc
                else:
                    return jsonify({
                        "error": "Certificado no válido",
                        "detalle": ocsp_result.get("errorMessage", "Certificado inactivo o revocado")
                    }), 400
        except Exception as e:
            return jsonify({"error": "Validación fallida", "detalle": str(e)}), 400

    if 'rfc' not in session:
        session['challenge'] = secrets.token_hex(4)

    return jsonify(dict(session))

@app.route('/submit', methods=['POST'])
def submit():
    if 'rfc' not in session:
        return "⚠️ Sesión no iniciada", 401

    nombre = request.form.get('nombreSolicitante')
    tipo_proyecto = request.form.get('tipoProyecto')
    archivo = request.files.get('documento')

    if not nombre or not archivo or not tipo_proyecto:
        return "Faltan datos requeridos", 400

    config = CONFIG_PROCESOS.get(tipo_proyecto)
    if not config:
        return f"Tipo de proyecto no válido: {tipo_proyecto}", 400

    container_id = config["containerId"]
    process_id = config["processId"]

    nombre_archivo = f"{uuid.uuid4()}_{archivo.filename}"
    ruta_completa = os.path.join(UPLOAD_FOLDER, nombre_archivo)
    archivo.save(ruta_completa)

    with open(ruta_completa, 'rb') as f:
        contenido_base64 = base64.b64encode(f.read()).decode('utf-8')

    size = os.path.getsize(ruta_completa)
    last_modified = int(os.path.getmtime(ruta_completa) * 1000)
    public_url = url_for('efirma_bp.descargar_documento', filename=nombre_archivo, _external=True)

    document_variable = {
        "org.jbpm.document.service.impl.DocumentImpl": {
            "identifier": str(uuid.uuid4()),
            "name": archivo.filename,
            "link": "",
            "size": size,
            "lastModified": last_modified,
            "content": contenido_base64
        }
    }

    payload = {
        "nombreSolicitante": nombre,
        "tipoProyecto": tipo_proyecto,
        "documento": document_variable,
        "georeferenciacionDelTerreno": public_url
    }

    credentials = f"{KIE_USERNAME}:{KIE_PASSWORD}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {encoded_credentials}",
        "X-KIE-ContentType": "JSON"
    }

    url = f"{KIE_SERVER_URL}/containers/{container_id}/processes/{process_id}/instances"
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 201:
        return render_template("redirect.html")
    else:
        return f"Error al iniciar el proceso: {response.status_code} - {response.text}", response.status_code

@efirma_bp.route('/documentos/<filename>')
def descargar_documento(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@efirma_bp.route('/documentos', methods=['POST'])
def recibir_documento():
    try:
        data = request.get_json(force=True)
        if not data or 'documentId' not in data:
            return jsonify({"error": "Falta el campo 'documentId'"}), 400

        document_id = data['documentId']
        print(f"✅ Recibido documentId: {document_id}")

        return jsonify({"estado": "recibido", "documentId": document_id}), 200

    except Exception as e:
        print(f"❌ Error interno: {e}")
        return jsonify({"error": "Error en el servidor", "detalle": str(e)}), 500




