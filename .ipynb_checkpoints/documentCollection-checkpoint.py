from flask import Flask, jsonify
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import sqlite3

app = Flask(__name__)

# Configuración de la base de datos SQLite
DATABASE = 'documents_collection.db'

# Parámetros de conexión al JBPM
JBPM_HOST = "http://localhost:8080"
CONTAINER_ID = "Publica_In_Out_1.0.0-SNAPSHOT"
USERNAME = "wbadmin"
PASSWORD = "wbadmin"

headers = {
    "Accept": "application/json"
}

def create_db():
    """Crea la base de datos y la tabla si no existen"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documentsCollection (
            processinstanceid TEXT,
            value TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_into_db(processinstanceid, value):
    """Inserta un nuevo registro en la tabla documentsCollection"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO documentsCollection (processinstanceid, value)
        VALUES (?, ?)
    ''', (processinstanceid, value))
    conn.commit()
    conn.close()

def get_documents(process_instance_id):
    """Obtiene los documentos desde el servidor JBPM y los inserta en la base de datos"""
    url = f"{JBPM_HOST}/kie-server/services/rest/server/containers/{CONTAINER_ID}/processes/instances/{process_instance_id}/variables"
    response = requests.get(url, headers=headers, auth=HTTPBasicAuth(USERNAME, PASSWORD))

    if response.status_code == 200:
        data = response.json()

        # Extraer documentos
        documents = data.get("documentosSETN", {}).get("documents", [])

        for doc in documents:
            doc_data = doc.get("org.jbpm.document.service.impl.DocumentImpl", {})
            name = doc_data.get("name", "sin_nombre")
            identifier = doc_data.get("identifier", "sin_id")
            value = f"{name}####{identifier}"

            # Insertar cada documento en la base de datos
            insert_into_db(process_instance_id, value)
    else:
        print(f"Error al obtener las variables del proceso {process_instance_id}: {response.status_code}")

@app.route('/actualizar_documentos/<process_instance_id>', methods=['GET'])
def actualizar_documentos(process_instance_id):
    """Endpoint para obtener documentos y actualizarlos en la base de datos"""
    get_documents(process_instance_id)
    return jsonify({"message": "Documentos actualizados exitosamente"}), 200

@app.route('/ver_documentos', methods=['GET'])
def ver_documentos():
    """Endpoint para ver todos los documentos en la base de datos"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM documentsCollection')
    rows = cursor.fetchall()
    conn.close()

    return jsonify(rows), 200

if __name__ == '__main__':
    create_db()  # Aseguramos que la DB y la tabla existan
    app.run(debug=True)
