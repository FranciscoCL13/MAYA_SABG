from flask import Flask, jsonify
import requests
from requests.auth import HTTPBasicAuth
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

# Parámetros de conexión a PostgreSQL
DB_USER = 'jbpm'
DB_PASSWORD = 'jbpm'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'jbpm'

# Crear conexión a la base de datos PostgreSQL usando SQLAlchemy
DATABASE_URI = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = create_engine(DATABASE_URI, echo=True)

# Declarando la base para el modelo
Base = declarative_base()

# Definir el modelo para la tabla `documentsCollection`
class DocumentCollection(Base):
    __tablename__ = 'documentsCollection'
    processinstanceid = Column(String, primary_key=True)
    value = Column(String)

# Crear la tabla si no existe
Base.metadata.create_all(engine)

# Crear una sesión para interactuar con la base de datos
Session = sessionmaker(bind=engine)
session = Session()

# Parámetros de conexión al JBPM
JBPM_HOST = "http://localhost:8080"
CONTAINER_ID = "Publica_In_Out_1.0.0-SNAPSHOT"
USERNAME = "wbadmin"
PASSWORD = "wbadmin"

headers = {
    "Accept": "application/json"
}

def insert_into_db(processinstanceid, value):
    """Inserta un nuevo registro en la tabla documentsCollection"""
    # Verificar si ya existe un documento con el mismo processinstanceid
    existing_doc = session.query(DocumentCollection).filter_by(processinstanceid=processinstanceid).first()
    if existing_doc:
        # Actualizar el valor si ya existe
        existing_doc.value = value
    else:
        # Si no existe, insertar un nuevo documento
        new_document = DocumentCollection(processinstanceid=processinstanceid, value=value)
        session.add(new_document)
    
    session.commit()

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
    documents = session.query(DocumentCollection).all()
    result = [{"processinstanceid": doc.processinstanceid, "value": doc.value} for doc in documents]
    return jsonify(result), 200

if __name__ == '__main__':
    # Imprimir las URLs de los endpoints antes de ejecutar la aplicación
    print("Endpoints disponibles:")
    print(f"  - /actualizar_documentos/<process_instance_id> (GET)")
    print(f"  - /ver_documentos (GET)")

    app.run(debug=True, port=5001)
