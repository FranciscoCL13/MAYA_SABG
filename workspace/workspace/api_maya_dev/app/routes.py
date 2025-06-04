from flask import Blueprint, request, jsonify, send_from_directory
from .functions import descargar_y_guardar_documento, obtener_lista_archivos
import os
from flask import current_app

bp = Blueprint("routes", __name__)

@bp.route('/documentos', methods=['POST'])
def recibir_documentos():
    try:
        data = request.get_json(force=True)
        ids = data.get("documentIds")

        if not ids or not isinstance(ids, list):
            return jsonify({"error": "Falta la lista 'documentIds'"}), 400

        resultados = []
        for document_id in ids:
            resultado = descargar_y_guardar_documento(document_id)
            resultados.append(resultado)

        return jsonify({"resultado": resultados}), 200

    except Exception as e:
        return jsonify({"error": "Error en el servidor", "detalle": str(e)}), 500

@bp.route('/files/<document_id>/<filename>')
def descargar_archivo(document_id, filename):
    carpeta = os.path.join(current_app.config['FILE_SERVER_PATH'], document_id)
    return send_from_directory(carpeta, filename, as_attachment=True)

@bp.route('/archivos')
def mostrar_archivos():
    filas = obtener_lista_archivos()
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
                {''.join([f"<tr><td>{archivo}</td><td><a href='{link}' target='_blank'>Descargar</a></td></tr>" for archivo, link in filas])}
            </tbody>
        </table>
    </body>
    </html>
    """
    return tabla
