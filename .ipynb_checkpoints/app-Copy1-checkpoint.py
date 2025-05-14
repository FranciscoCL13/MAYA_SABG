from flask import Flask, render_template, jsonify, send_from_directory
from sqlalchemy import create_engine
import pandas as pd
import os

app = Flask(__name__)

# Ruta base donde están los archivos compartidos por jBPM
ARCHIVOS_BASE_DIR = r"Z:\jbpm_docs"

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

# Ruta para descargar archivos según carpeta dinámica (fecha/uuid)
@app.route('/descargar/<fecha>/<uuid>/<filename>')
def descargar_archivo(fecha, uuid, filename):
    try:
        ruta_carpeta = os.path.join(ARCHIVOS_BASE_DIR, fecha, uuid)
        return send_from_directory(ruta_carpeta, filename, as_attachment=True)
    except FileNotFoundError:
        return f"<p style='color:red;'>Archivo no encontrado en ruta esperada: {ruta_carpeta}</p>"

@app.route('/generar_tabla', methods=['GET'])
def generar_tabla():
    try:
        # Consulta que une taskvariableimpl con task y extrae los valores necesarios
        consulta_sql = """
            SELECT
                task.actualowner_id AS usuario,
                numero_catastral.value AS numero_catastral,
                taskvariableimpl.value,
                task.name,
                taskvariableimpl.processid
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

        # Función para extraer el nombre, fecha y UUID del campo value
        def extraer_componentes(valor):
            try:
                partes = valor.split('####')
                nombre = partes[0]
                fecha = partes[2][:10]  # Tomamos solo la parte de fecha
                uuid = partes[3]
                return nombre, fecha, uuid
            except Exception:
                return None, None, None

        # Generar botón HTML si existe el archivo
        def generar_html_descarga(valor):
            nombre, fecha, uuid = extraer_componentes(valor)
            if all([nombre, fecha, uuid]):
                ruta_archivo = os.path.join(ARCHIVOS_BASE_DIR, fecha, uuid, nombre)
                if os.path.isfile(ruta_archivo):
                    url = f"/descargar/{fecha}/{uuid}/{nombre}"
                    return f'<a href="{url}" class="btn btn-sm btn-primary" target="_blank">{nombre}</a>'
            return valor  # Si no cumple condiciones, se regresa el valor original

        # Aplicamos la transformación a la columna 'value'
        df['value'] = df['value'].apply(generar_html_descarga)

        # Guardamos la tabla transformada en la base
        df.to_sql(
            name='x_mi_tabla_completa',
            con=engine,
            if_exists='replace',
            index=False
        )

        # Renderizado HTML
        nombre_tabla = "<h3>Tabla:</h3> <h1>x_mi_tabla_completa</h1><a> Se generó y almacenó en base de datos</a><hr>"
        tabla_html = df.to_html(classes='table table-bordered', index=False, escape=False)

        return jsonify({'tabla': nombre_tabla + tabla_html})

    except Exception as e:
        return jsonify({'tabla': f"<p style='color:red;'>Error al generar o almacenar la tabla: {e}</p>"})

if __name__ == '__main__':
    app.run(debug=True)
