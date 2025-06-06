from flask import Flask, request, render_template, send_from_directory, url_for
import requests
import base64
import uuid
import time
import os

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploaded_docs')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

KIE_SERVER_URL = "http://172.25.30.94:8080/kie-server/services/rest/server"
CONTAINER_ID = "Publica_In_Out_1.0.0-SNAPSHOT"
PROCESS_ID = "Publica_In_Out.Publica"
KIE_USERNAME = "wbadmin"
KIE_PASSWORD = "wbadmin"

@app.route('/')
def index():
    return render_template('form3.html')

@app.route('/submit', methods=['POST'])
def submit():
    nombre = request.form.get('nombreSolicitante')
    tipo_proyecto = request.form.get('tipoProyecto')
    archivo = request.files.get('documento')

    if not nombre or not archivo or not tipo_proyecto:
        return "Faltan datos requeridos", 400

    # Guardar el archivo localmente
    nombre_archivo = f"{uuid.uuid4()}_{archivo.filename}"
    ruta_completa = os.path.join(UPLOAD_FOLDER, nombre_archivo)
    archivo.save(ruta_completa)

    # Leer y codificar en base64
    with open(ruta_completa, 'rb') as f:
        contenido_base64 = base64.b64encode(f.read()).decode('utf-8')

    size = os.path.getsize(ruta_completa)
    last_modified = int(os.path.getmtime(ruta_completa) * 1000)

    # URL pública del archivo
    public_url = url_for('descargar_documento', filename=nombre_archivo, _external=True)

    # Documento como objeto DocumentImpl
    document_variable = {
        "org.jbpm.document.service.impl.DocumentImpl": {
            "identifier": str(uuid.uuid4()),
            "name": archivo.filename,
            "link": "",  # Campo link vacío en DocumentImpl
            "size": size,
            "lastModified": last_modified,
            "content": contenido_base64
        }
    }

    # Variables del proceso
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

    url = f"{KIE_SERVER_URL}/containers/{CONTAINER_ID}/processes/{PROCESS_ID}/instances"
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 201:
        return (
            f"Proceso iniciado correctamente. ID: {response.text}<br>"
            f"Documento disponible en: <a href='{public_url}' target='_blank'>{public_url}</a><br>"
            f"Tipo de Proyecto: {tipo_proyecto}"
        )
    else:
        return f"Error al iniciar el proceso: {response.status_code} - {response.text}", response.status_code

@app.route('/documentos/<filename>')
def descargar_documento(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
