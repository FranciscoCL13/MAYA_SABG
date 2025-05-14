from flask import Flask, render_template, jsonify, send_from_directory
from sqlalchemy import create_engine
import pandas as pd
import os
import json

app = Flask(__name__)

# Ruta donde se encuentran todos los archivos sin subdirectorios
ARCHIVOS_BASE_DIR = r"C:\\Users\\francisco.contreras\\Desktop\\jupyter-projects\\notebooks\\archivosAdjuntos"

# Configuración de conexión a PostgreSQL
user = 'jbpm'
password = 'jbpm'
host = 'localhost'
port = '5432'
database = 'jbpm'
engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/descargar/<filename>')
def descargar_archivo(filename):
    try:
        return send_from_directory(ARCHIVOS_BASE_DIR, filename, as_attachment=True)
    except FileNotFoundError:
        return f"<p style='color:red;'>Archivo no encontrado en {ARCHIVOS_BASE_DIR}</p>"

def extraer_documentos(valor):
    nombres = []
    try:
        doc_data = json.loads(valor.replace("'", '"'))  # Intento de parseo básico
        if isinstance(doc_data, dict):
            if "documents" in doc_data:
                for doc_wrapper in doc_data["documents"]:
                    doc = list(doc_wrapper.values())[0]
                    nombre = doc.get("name")
                    if nombre:
                        nombres.append(nombre)
            elif "name" in doc_data:
                nombre = doc_data.get("name")
                if nombre:
                    nombres.append(nombre)
    except Exception:
        pass
    return nombres

def generar_html_descarga(nombre_archivo):
    if nombre_archivo:
        ruta_archivo = os.path.join(ARCHIVOS_BASE_DIR, nombre_archivo)
        if os.path.isfile(ruta_archivo):
            url = f"/descargar/{nombre_archivo}"
            return f'<a href="{url}" class="btn btn-sm btn-primary" target="_blank">{nombre_archivo}</a>'
    return nombre_archivo

@app.route('/generar_tabla', methods=['GET'])
def generar_tabla():
    try:
        consulta_sql = """
            SELECT
                task.actualowner_id AS usuario,
                numero_catastral.value AS numero_catastral,
                taskvariableimpl.value,
                task.name,
                taskvariableimpl.processid,
                taskvariableimpl.processinstanceid
            FROM taskvariableimpl
            JOIN task
                ON taskvariableimpl.processinstanceid = task.processinstanceid
                AND taskvariableimpl.taskid = task.id
            LEFT JOIN (
                SELECT
                    processinstanceid,
                    value
                FROM taskvariableimpl
                WHERE name = 'numero_oficio'
            ) AS numero_catastral
                ON numero_catastral.processinstanceid = taskvariableimpl.processinstanceid
            WHERE taskvariableimpl.value LIKE %(patron)s or taskvariableimpl.value LIKE %(patronDos)s
            ORDER BY taskvariableimpl.processinstanceid;
        """
        df = pd.read_sql(consulta_sql, engine, params={"patron": "%####%", "patronDos": "%@%"})

        def procesar_valor(valor):
            nombres = extraer_documentos(valor)
            if nombres:
                return '<br>'.join([generar_html_descarga(n) for n in nombres])
            return valor

        df['value'] = df['value'].apply(procesar_valor)

        df.to_sql(
            name='x_mi_tabla_completa',
            con=engine,
            if_exists='replace',
            index=False
        )

        nombre_tabla = "<h3>Tabla:</h3> <h1>x_mi_tabla_completa</h1><a> Se generó y almacenó en base de datos</a><hr>"
        tabla_html = df.to_html(classes='table table-bordered', index=False, escape=False)

        return jsonify({'tabla': nombre_tabla + tabla_html})

    except Exception as e:
        return jsonify({'tabla': f"<p style='color:red;'>Error al generar o almacenar la tabla: {e}</p>"})

if __name__ == '__main__':
    app.run(debug=True)
