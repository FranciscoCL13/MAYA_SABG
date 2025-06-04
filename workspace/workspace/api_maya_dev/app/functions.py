import os
import base64
import requests
from werkzeug.utils import secure_filename
from flask import current_app

def obtener_headers():
    credentials = f"{current_app.config['KIE_USERNAME']}:{current_app.config['KIE_PASSWORD']}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    return {
        "binary": {
            "Authorization": f"Basic {encoded_credentials}"
        },
        "json": {
            "Authorization": f"Basic {encoded_credentials}",
            "Accept": "application/json"
        }
    }

def descargar_y_guardar_documento(document_id):
    KIE_SERVER_URL = current_app.config['KIE_SERVER_URL']
    FILE_SERVER_PATH = current_app.config['FILE_SERVER_PATH']
    headers = obtener_headers()

    content_url = f"{KIE_SERVER_URL}/documents/{document_id}/content"
    response = requests.get(content_url, headers=headers['binary'])
    if response.status_code != 200:
        return {"documentId": document_id, "error": "No se pudo recuperar el contenido"}

    metadata_url = f"{KIE_SERVER_URL}/documents/{document_id}"
    metadata_response = requests.get(metadata_url, headers=headers['json'])
    if metadata_response.status_code == 200:
        try:
            metadata = metadata_response.json()
            nombre_archivo = secure_filename(metadata.get("document-name", f"{document_id}.bin"))
        except Exception:
            nombre_archivo = f"{document_id}.bin"
    else:
        nombre_archivo = f"{document_id}.bin"

    carpeta_documento = os.path.join(FILE_SERVER_PATH, document_id)
    os.makedirs(carpeta_documento, exist_ok=True)

    file_path = os.path.join(carpeta_documento, nombre_archivo)
    with open(file_path, "wb") as f:
        f.write(response.content)

    return {"documentId": document_id, "archivo": file_path}

def obtener_lista_archivos():
    FILE_SERVER_PATH = current_app.config['FILE_SERVER_PATH']
    filas = []

    for document_id in os.listdir(FILE_SERVER_PATH):
        carpeta = os.path.join(FILE_SERVER_PATH, document_id)
        if not os.path.isdir(carpeta):
            continue

        for archivo in os.listdir(carpeta):
            link = f"/files/{document_id}/{archivo}"
            filas.append((archivo, link))
    return filas
