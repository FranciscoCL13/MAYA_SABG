from flask import Flask, request, jsonify, send_from_directory
import requests
import base64
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

KIE_SERVER_URL = "http://172.25.30.98:8080/kie-server/services/rest/server"
KIE_USERNAME = "wbadmin"
KIE_PASSWORD = "wbadmin"
FILE_SERVER_PATH = "/MayaPruebaAdjuntos"

@app.route('/documentos', methods=['POST'])
def recibir_documentos():
    try:
        data = request.get_json(force=True)
        ids = data.get("documentIds")

        if not ids or not isinstance(ids, list):
            return jsonify({"error": "Falta la lista 'documentIds'"}), 400

        resultados = []

        credentials = f"{KIE_USERNAME}:{KIE_PASSWORD}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        headers_binary = {
            "Authorization": f"Basic {encoded_credentials}"
        }

        headers_metadata = {
            "Authorization": f"Basic {encoded_credentials}",
            "Accept": "application/json"
        }

        for document_id in ids:
            print(f"✅ Procesando documentId: {document_id}")

            content_url = f"{KIE_SERVER_URL}/documents/{document_id}/content"
            response = requests.get(content_url, headers=headers_binary)
            if response.status_code != 200:
                resultados.append({"documentId": document_id, "error": "No se pudo recuperar el contenido"})
                continue

            metadata_url = f"{KIE_SERVER_URL}/documents/{document_id}"
            metadata_response = requests.get(metadata_url, headers=headers_metadata)
            if metadata_response.status_code == 200:
                try:
                    metadata = metadata_response.json()
                    nombre_archivo = metadata.get("document-name", f"{document_id}.bin")
                    nombre_archivo = secure_filename(nombre_archivo)
                    print(f"📎 Nombre recuperado: {nombre_archivo}")
                except Exception as e:
                    print(f"⚠️ Error al parsear metadata: {e}")
                    nombre_archivo = f"{document_id}.bin"
            else:
                print("⚠️ No se pudo obtener metadata, se usará nombre por defecto")
                nombre_archivo = f"{document_id}.bin"

            carpeta_documento = os.path.join(FILE_SERVER_PATH, document_id)
            os.makedirs(carpeta_documento, exist_ok=True)

            file_path = os.path.join(carpeta_documento, nombre_archivo)
            with open(file_path, "wb") as f:
                f.write(response.content)

            print(f"✅ Guardado: {file_path}")
            resultados.append({
                "documentId": document_id,
                "archivo": file_path
            })

        return jsonify({"resultado": resultados}), 200

    except Exception as e:
        print(f"❌ Error interno: {e}")
        return jsonify({"error": "Error en el servidor", "detalle": str(e)}), 500

@app.route('/files/<document_id>/<filename>')
def descargar_archivo(document_id, filename):
    carpeta = os.path.join(FILE_SERVER_PATH, document_id)
    return send_from_directory(carpeta, filename, as_attachment=True)

@app.route('/archivos')
def mostrar_archivos():
    filas = []

    for document_id in os.listdir(FILE_SERVER_PATH):
        carpeta = os.path.join(FILE_SERVER_PATH, document_id)
        if not os.path.isdir(carpeta):
            continue

        for archivo in os.listdir(carpeta):
            link = f"/files/{document_id}/{archivo}"
            filas.append(f"<tr><td>{archivo}</td><td><a href='{link}' target='_blank'>Descargar</a></td></tr>")

    tabla = f"""
    <html>
    <head><title>Archivos disponibles</title></head>
    <body>
        <h2>📁 Lista de Archivos Guardados</h2>
        <table border="1" cellpadding="8" cellspacing="0">
            <thead>
                <tr><th>Nombre del Archivo</th><th>Enlace</th></tr>
            </thead>
            <tbody>
                {''.join(filas)}
            </tbody>
        </table>
    </body>
    </html>
    """
    return tabla

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081)
