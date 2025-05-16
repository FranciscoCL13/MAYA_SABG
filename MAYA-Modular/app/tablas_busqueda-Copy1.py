from flask import Blueprint, render_template, jsonify, send_from_directory
from sqlalchemy import text
import pandas as pd
import os
import json
from app.conexion import get_engine

tablas_bp = Blueprint('tablas_bp', __name__, template_folder='templates')

ARCHIVOS_BASE_DIR = r"C:\Users\francisco.contreras\Desktop\jupyter-projects\notebooks\archivosAdjuntos"

engine = get_engine()

@tablas_bp.route('/')
def index():
    return render_template('index.html')

@tablas_bp.route('/descargar/<path:filename>')  # path: para permitir subdirectorios si hay
def descargar_archivo(filename):
    try:
        return send_from_directory(ARCHIVOS_BASE_DIR, filename, as_attachment=True)
    except FileNotFoundError:
        return f"<p style='color:red;'>Archivo no encontrado en {ARCHIVOS_BASE_DIR}</p>", 404

def extraer_documentos(valor):
    nombres = []
    try:
        # Normaliza comillas simples a dobles para json.loads
        doc_data = json.loads(valor.replace("'", '"'))
        if isinstance(doc_data, dict):
            if "documents" in doc_data:
                for doc_wrapper in doc_data["documents"]:
                    # doc_wrapper es dict con un solo par clave-valor
                    doc = list(doc_wrapper.values())[0]
                    nombre = doc.get("name")
                    if nombre:
                        nombres.append(nombre)
            elif "name" in doc_data:
                nombre = doc_data.get("name")
                if nombre:
                    nombres.append(nombre)
    except Exception:
        pass  # Podrías agregar logging aquí si quieres
    return nombres

def generar_html_descarga(nombre_archivo):
    if nombre_archivo:
        ruta_archivo = os.path.join(ARCHIVOS_BASE_DIR, nombre_archivo)
        if os.path.isfile(ruta_archivo):
            url = f"/tablas/descargar/{nombre_archivo}"
            return f'<a href="{url}" class="btn btn-sm btn-primary" target="_blank" rel="noopener noreferrer">{nombre_archivo}</a>'
    return nombre_archivo

@tablas_bp.route('/generar_tabla', methods=['GET'])
def generar_tabla():
    try:
        consulta_sql = text("""
            SELECT
                task.actualowner_id AS usuario,
                numero_catastral.value AS numero_catastral,
                taskvariableimpl.value,
                task.name,
                taskvariableimpl.processid,
                taskvariableimpl.processinstanceid,
                taskvariableimpl.name as variable
            FROM taskvariableimpl
            JOIN task
                ON taskvariableimpl.processinstanceid = task.processinstanceid
                AND taskvariableimpl.taskid = task.id
            LEFT JOIN (
                SELECT
                    processinstanceid,
                    value
                FROM taskvariableimpl
                WHERE name = 'numero_catastral'
            ) AS numero_catastral
                ON numero_catastral.processinstanceid = taskvariableimpl.processinstanceid
            WHERE taskvariableimpl.value LIKE :patron OR taskvariableimpl.value LIKE :patronDos
            ORDER BY taskvariableimpl.processinstanceid;
        """)

        df = pd.read_sql(consulta_sql, engine, params={"patron": "%####%", "patronDos": "%@%"})

        # Aplica función para convertir valores que parecen contener documentos a enlaces de descarga
        df['value'] = df['value'].apply(
            lambda v: '<br>'.join([generar_html_descarga(n) for n in extraer_documentos(v)]) if extraer_documentos(v) else v
        )

        # Guarda la tabla en base de datos (sobrescribe si ya existe)
        df.to_sql('x_mi_tabla_completa', engine, if_exists='replace', index=False)

        tabla_html = df.to_html(classes='table table-bordered', index=False, escape=False)
        return jsonify({'tabla': f"<h3>Tabla:</h3><h1>x_mi_tabla_completa</h1><a> Se generó y almacenó en base de datos</a><hr>{tabla_html}"})

    except Exception as e:
        return jsonify({'tabla': f"<p style='color:red;'>Error al generar o almacenar la tabla: {str(e)}</p>"}), 500
