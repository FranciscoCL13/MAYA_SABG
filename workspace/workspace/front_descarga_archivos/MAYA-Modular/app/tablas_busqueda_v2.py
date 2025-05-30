from flask import Blueprint, render_template, jsonify, send_file, abort, request, session
from sqlalchemy import text
import pandas as pd
import os
import json
import re
from app.conexion import get_engine
import subprocess

tablas_bp = Blueprint('tablas_bp', __name__, template_folder='templates')

# Ruta base de archivos
ARCHIVOS_BASE_DIR = r"/MayaPruebaAdjuntos"

engine = get_engine()

# -------------------------------------------------------------------------------------------

@tablas_bp.route('/')
def index():
    return render_template('index.html')

@tablas_bp.route('/descargar/<usuario>/<id_carpeta>/<nombre_archivo>')
def descargar_archivo(usuario, id_carpeta, nombre_archivo):
    # Construir ruta con base, id y nombre archivo
    ruta_completa = os.path.join(ARCHIVOS_BASE_DIR, id_carpeta, nombre_archivo)
    if os.path.isfile(ruta_completa):
        return send_file(ruta_completa, as_attachment=True)
    return f"<p style='color:red;'>Archivo <b>{nombre_archivo}</b> no encontrado en {ruta_completa}</p>", 404

# -------------------------------------------------------------------------------------------

def extraer_nombre_id(valor):
    """
    De 'ip_config.out#175781026' devuelve ('ip_config.out', '175781026')
    """
    if not valor or '#' not in valor:
        return valor, None
    nombre, id_carpeta = valor.split('#', 1)
    return nombre.strip(), id_carpeta.strip()

def generar_html_descarga(usuario, valor):
    """
    Genera el link de descarga basado en usuario, id y nombre archivo.
    """
    nombre_archivo, id_carpeta = extraer_nombre_id(valor)
    if nombre_archivo and id_carpeta:
        url = f"/tablas/descargar/{usuario}/{id_carpeta}/{nombre_archivo}"
        return f'<a href="{url}" class="btn btn-sm btn-primary" target="_blank" rel="noopener noreferrer">{nombre_archivo}</a>'
    else:
        return valor

def limpiar_nombre_archivo(texto, usuario):
    """
    Aplica extracción y armado del link para cada valor de archivo.
    """
    if isinstance(texto, str):
        # Puede venir en formato JSON con documentos
        try:
            nombres = []
            doc_data = json.loads(texto.replace("'", '"'))
            if isinstance(doc_data, dict):
                if "documents" in doc_data:
                    for doc_wrapper in doc_data["documents"]:
                        doc = list(doc_wrapper.values())[0]
                        nombre = doc.get("name")
                        if nombre:
                            nombres.append(generar_html_descarga(usuario, nombre))
                elif "name" in doc_data:
                    nombre = doc_data.get("name")
                    if nombre:
                        nombres.append(generar_html_descarga(usuario, nombre))
            if nombres:
                return '<br>'.join(nombres)
        except Exception:
            # No es JSON, seguir con texto plano
            pass

        # En texto plano, puede tener separador '####', tomar antes
        nombre_limpio = re.split(r'####', texto)[0].strip()
        return generar_html_descarga(usuario, nombre_limpio)

    return texto

# -------------------------------------------------------------------------------------------
@tablas_bp.route('/generar_tabla', methods=['GET'])
def generar_tabla():
    try:
        # Obtener usuario logueado, aquí puedes adaptar según tu autenticación
        userLoggin = request.args.get('usuario', 'katy')  # Ejemplo, cambiar a sesión o lo que uses

        # Ejecutar scripts sin interrumpir la ejecución si fallan
        try:
            if not ejecutar_script('MAYA-Modular-scripts-copiar_completo_CC.sh'):
                print("[WARNING] Error al ejecutar script de copiado")
        except Exception as e:
            print(f"[ERROR] Falló ejecución de copiado: {e}")

        try:
            if not ejecutar_script('limpiar_jbpm_docs_localADocker.sh'):
                print("[WARNING] Error al ejecutar script de limpieza")
        except Exception as e:
            print(f"[ERROR] Falló ejecución de limpieza: {e}")

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
            WHERE v.variableinstanceid LIKE 'doc%'
              AND t.actualowner_id = :usuario
            ORDER BY modificationdate desc;
        """)

        df_final = pd.read_sql(combinacion_sql, engine, params={'usuario': userLoggin})
        df_final.to_sql('x_mi_tabla_combinada', engine, if_exists='replace', index=False)

        # Limpiar y armar los links dinámicamente
        df_final['value'] = df_final['value'].apply(lambda x: limpiar_nombre_archivo(x, userLoggin))
        df_final = df_final.rename(columns={
            'value': 'Descargar archivo',
            'modificationdate': 'Fecha de carga'
        })

        total_registros = len(df_final)
        conteo_html = f"<p>Registros encontrados para <b>{userLoggin}</b>: <strong>{total_registros}</strong></p>"

        tabla_html = df_final.to_html(classes='table table-bordered', index=False, escape=False)
        return jsonify({'tabla': f"<h3 style='display:none;'>x_mi_tabla_combinada:</h3>{conteo_html}<hr>{tabla_html}"})

    except Exception as e:
        return jsonify({'tabla': f"<p style='color:red;'>Error: {str(e)}</p>"}), 500

# ----------------------------------------------------------------------------------
@tablas_bp.route('/buscar_tabla', methods=['GET'])
def buscar_tabla():
    numero = request.args.get('numero_catastral', '').strip()
    userLoggin = request.args.get('usuario', 'katy')  # Obtener usuario, adaptar a tu autenticación

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
              AND usuario = :usuario
            ORDER BY modificationdate;
        """)
        df_filtro = pd.read_sql(consulta_sql, engine, params={'numero': f"%{numero}%", 'usuario': userLoggin})
        if df_filtro.empty:
            return jsonify({'tabla': f'<p>No se encontraron resultados para el número catastral: <strong>{numero}</strong></p>'})

        df_filtro['value'] = df_filtro['value'].apply(lambda x: limpiar_nombre_archivo(x, userLoggin))
        df_filtro = df_filtro.rename(columns={
            'value': 'Descargar archivo',
            'modificationdate': 'Fecha de carga'
        })

        total_filtrados = len(df_filtro)
        conteo_html = f"<p>Registros encontrados para <b>{userLoggin}</b>: <strong>{total_filtrados}</strong></p>"

        tabla_html = df_filtro.to_html(classes='table table-bordered', index=False, escape=False)
        return jsonify({'tabla': f"<h3>Resultados filtrados por número catastral: {numero}</h3>{conteo_html}<hr>{tabla_html}"})

    except Exception as e:
        return jsonify({'tabla': f"<p style='color:red;'>Error al buscar: {str(e)}</p>"}), 500

# ----------------------------------------------------------------------------------

def ejecutar_script(nombre_script):
    """
    Ejecuta un script .sh y devuelve True si fue exitoso.
    """
    try:
        resultado = subprocess.run(['bash', nombre_script], capture_output=True, text=True)
        if resultado.returncode != 0:
            print(f"[ERROR] Script {nombre_script} falló:\n{resultado.stderr}")
            return False
        return True
    except Exception as e:
        print(f"[EXCEPCIÓN] al ejecutar script {nombre_script}: {e}")
        return False
