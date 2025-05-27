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
KIE_USERNAME = "wbadmin"
KIE_PASSWORD = "wbadmin"

# Mapeo de containerId y processId por tipo de proyecto
CONFIG_PROCESOS = {
    "Público": {
        "containerId": "Publica_In_Out_1.0.0-SNAPSHOT",
        "processId": "Publica_In_Out.Publica"
    },
    "Privado": {
        "containerId": "Privada_1.0.0-SNAPSHOT",
        "processId": "Publica.Privada_In_Out"
    },
    "Social": {
        "containerId": "Social_In_Out_1.0.0-SNAPSHOT",
        "processId": "Social_In_Out.Social"
    }
}

@app.route('/')
def index():
    return render_template('form5.html')

@app.route('/submit', methods=['POST'])
def submit():
    nombre = request.form.get('nombreSolicitante')
    tipo_proyecto = request.form.get('tipoProyecto')
    archivo = request.files.get('documento')

    if not nombre or not archivo or not tipo_proyecto:
        return "Faltan datos requeridos", 400

    # Obtener containerId y processId según tipo de proyecto
    config = CONFIG_PROCESOS.get(tipo_proyecto)
    if not config:
        return f"Tipo de proyecto no válido: {tipo_proyecto}", 400

    container_id = config['containerId']
    process_id = config['processId']

    # Guardar archivo localmente
    nombre_archivo = f"{uuid.uuid4()}_{archivo.filename}"
    ruta_completa = os.path.join(UPLOAD_FOLDER, nombre_archivo)
    archivo.save(ruta_completa)

    # Leer y codificar en base64
    with open(ruta_completa, 'rb') as f:
        contenido_base64 = base64.b64encode(f.read()).decode('utf-8')

    size = os.path.getsize(ruta_completa)
    last_modified = int(os.path.getmtime(ruta_completa) * 1000)
    public_url = url_for('descargar_documento', filename=nombre_archivo, _external=True)

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
       return redirect("http://172.25.30.94:8080/business-central/kie-wb.jsp?standalone=false&perspective=Tasks")
#        return (
#            f"Proceso iniciado correctamente. ID: {response.text}<br>"
#            f"Documento disponible en: <a href='{public_url}' target='_blank'>{public_url}</a><br>"
#            f"Tipo de Proyecto: {tipo_proyecto}"
#        )
    else:
        return f"Error al iniciar el proceso: {response.status_code} - {response.text}", response.status_code

@app.route('/documentos/<filename>')
def descargar_documento(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
