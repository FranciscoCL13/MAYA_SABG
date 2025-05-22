from flask import Blueprint, render_template, jsonify, send_file, abort, request
from sqlalchemy import text
import pandas as pd
import os
import json
from app.conexion import get_engine
import re

tablas_bp = Blueprint('tablas_bp', __name__, template_folder='templates')

# Ruta base de archivos
ARCHIVOS_BASE_DIR = r"C:\User\francisco.contreras\Desktop\jupyter-projects\notebooks\archivosAdjuntos"
ARCHIVOS_BASE_DIR = r"\server"

# ARCHIVOS_BASE_DIR = "/app/archivosAdjuntos"

engine = get_engine()

##-------------------------------------------------------------------------------------------
@tablas_bp.route('/')
def index():
    return render_template('index.html')

@tablas_bp.route('/descargar/<path:filename>')
def descargar_archivo(filename):
    # Busca recursivamente en subdirectorios
    for root, dirs, files in os.walk(ARCHIVOS_BASE_DIR):
        if filename in files:
            ruta_completa = os.path.join(root, filename)
            return send_file(ruta_completa, as_attachment=True)
    return f"<p style='color:red;'>Archivo <b>{filename}</b> no encontrado en {ARCHIVOS_BASE_DIR}</p>", 404

##-------------------------------------------------------------------------------------------
def extraer_documentos(valor):
    nombres = []
    try:
        doc_data = json.loads(valor.replace("'", '"'))
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

##---------------------------------------------------------------------------------------------
def generar_html_descarga(nombre_archivo):
    if nombre_archivo:
        url = f"/tablas/descargar/{nombre_archivo}"
        return f'<a href="{url}" class="btn btn-sm btn-primary" target="_blank" rel="noopener noreferrer">{nombre_archivo}</a>'
    return nombre_archivo

# -------------------------------------------------------------------------------------------
def limpiar_nombre_archivo(texto):
    nombres = extraer_documentos(texto)
    if nombres:
        return '<br>'.join([generar_html_descarga(n) for n in nombres])

    if isinstance(texto, str):
        nombre_limpio = re.split(r'####', texto)[0].strip()
        return generar_html_descarga(nombre_limpio)

    return texto

## -------------------------------------------------------------------------------------------
@tablas_bp.route('/generar_tabla', methods=['GET'])
def generar_tabla():
    try:
        # 1. Genera la tabla base
        # 2. tabla combinada
        combinacion_sql = text("""
            select distinct 
                nc.value AS numero_catastral,
                
                t.actualowner_id as usuario,
                v.value,
                
                tv.modificationdate
                
            FROM variableinstancelog v
            JOIN task t ON v.processinstanceid = t.processinstanceid
            LEFT JOIN taskvariableimpl tv
                ON v.processinstanceid = tv.processinstanceid
                AND v.variableinstanceid = tv.name
            LEFT JOIN (
                SELECT processinstanceid, value
                FROM taskvariableimpl
                WHERE name = 'numero_catastral'
            ) nc ON v.processinstanceid = nc.processinstanceid
            WHERE v.variableinstanceid LIKE 'documento%'
            ORDER BY numero_catastral;
        """)

        df_final = pd.read_sql(combinacion_sql, engine)
        df_final.to_sql('x_mi_tabla_combinada', engine, if_exists='replace', index=False)

        # 3. Agrega enlaces de descarga con nombres limpios
        df_final['value'] = df_final['value'].apply(limpiar_nombre_archivo)
        #Cambiar nombre a columnas
        df_final = df_final.rename(columns={
            'value': 'Descargar archivo',
            'modificationdate': 'Fecha de carga'
        })

        total_registros = len(df_final)
        conteo_html = f"<p>Registros encontrados: <strong>{total_registros}</strong></p>"

        tabla_html = df_final.to_html(classes='table table-bordered', index=False, escape=False)
        return jsonify({'tabla': f"<h3>x_mi_tabla_combinada:</h3>{conteo_html}<hr>{tabla_html}"})

    except Exception as e:
        return jsonify({'tabla': f"<p style='color:red;'>Error: {str(e)}</p>"}), 500

## ----------------------------------------------------------------------------------
@tablas_bp.route('/buscar_tabla', methods=['GET'])
def buscar_tabla():
    numero = request.args.get('numero_catastral', '').strip()
    if not numero:
        return jsonify({'tabla': '<p style="color:red;">Número catastral no proporcionado</p>'}), 400

    try:
        consulta_sql = text("""
            SELECT 
                numero_catastral,
                usuario,
                value,
                modificationdate
            FROM x_mi_tabla_combinada
            WHERE numero_catastral LIKE :numero
            ORDER BY modificationdate;
        """)
        df_filtro = pd.read_sql(consulta_sql, engine, params={'numero': f"%{numero}%"})
        if df_filtro.empty:
            return jsonify({'tabla': f'<p>No se encontraron resultados para el número catastral: <strong>{numero}</strong></p>'})

        df_filtro['value'] = df_filtro['value'].apply(limpiar_nombre_archivo)
        #Cambiar nombre a columnas
        df_filtro = df_filtro.rename(columns={
            'value': 'Descargar archivo',
            'modificationdate': 'Fecha de carga'
        })

        total_filtrados = len(df_filtro)
        conteo_html = f"<p>Registros encontrados: <strong>{total_filtrados}</strong></p>"

        tabla_html = df_filtro.to_html(classes='table table-bordered', index=False, escape=False)
        return jsonify({'tabla': f"<h3>Resultados filtrados por número catastral: {numero}</h3>{conteo_html}<hr>{tabla_html}"})

    except Exception as e:
        return jsonify({'tabla': f"<p style='color:red;'>Error al buscar: {str(e)}</p>"}), 500