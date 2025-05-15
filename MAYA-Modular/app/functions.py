# functions.py
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
from sqlalchemy import inspect
from app.conexion import get_engine


# Parámetros de conexión a jBPM
JBPM_HOST = "http://localhost:8080"
USERNAME = "wbadmin"
PASSWORD = "wbadmin"
CONTAINER_ID = "Publica_In_Out_1.0.0-SNAPSHOT"

headers = {
    "Accept": "application/json"
}

def get_latest_process_instance():
    url = f"{JBPM_HOST}/kie-server/services/rest/server/queries/processes/instances?status=1&page=0&pageSize=10"
    response = requests.get(url, headers=headers, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    if response.status_code == 200:
        instances = response.json().get("process-instance", [])
        if instances:
            return instances[0].get("process-instance-id")
    return None

def get_all_documents(process_instance_id):
    url = f"{JBPM_HOST}/kie-server/services/rest/server/containers/{CONTAINER_ID}/processes/instances/{process_instance_id}/variables"
    response = requests.get(url, headers=headers, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    resultados = []

    if response.status_code == 200:
        data = response.json()
        for var_name, var_value in data.items():
            if isinstance(var_value, dict) and "documents" in var_value:
                for doc in var_value["documents"]:
                    doc_data = doc.get("org.jbpm.document.service.impl.DocumentImpl", {})
                    name = doc_data.get("name", "sin_nombre")
                    identifier = doc_data.get("identifier", "sin_id")
                    date = doc_data.get("lastModified", {}).get("java.util.Date", None)
                    value = f"{name}####{identifier}"
                    resultados.append({
                        "processinstanceid": process_instance_id,
                        "value": value,
                        "lastModified": date,
                        "variable": var_name,
                        "identifier": identifier
                    })
    else:
        print(f"Error al obtener variables del proceso {process_instance_id}: {response.status_code}")
        print(response.text)

    return resultados

def extract_and_store_documents():
    process_instance_id = get_latest_process_instance()
    if process_instance_id:
        docs = get_all_documents(process_instance_id)
        dfCollect = pd.DataFrame(docs)
        print(dfCollect)
    else:
        print("No se encontró ningún proceso activo.")
        dfCollect = pd.DataFrame()

    engine = get_engine()

    if not dfCollect.empty:
        with engine.connect() as conn:
            inspector = inspect(engine)
            tables = inspector.get_table_names()

            if 'tabla_document_collections' not in tables:
                dfCollect.to_sql(
                    name='tabla_document_collections',
                    con=engine,
                    if_exists='replace',
                    index=False
                )
                print("Tabla creada e información insertada.")
            else:
                existing_identifiers = pd.read_sql(
                    'SELECT identifier FROM tabla_document_collections',
                    con=engine
                )['identifier'].astype(str).tolist()

                df_nuevos = dfCollect[~dfCollect['identifier'].astype(str).isin(existing_identifiers)]

                if not df_nuevos.empty:
                    df_nuevos.to_sql(
                        name='tabla_document_collections',
                        con=engine,
                        if_exists='append',
                        index=False
                    )
                    print(f"{len(df_nuevos)} documento(s) insertado(s) exitosamente.")
                else:
                    print("No hay nuevos documentos para insertar (identifiers ya existentes).")
    else:
        print("No se encontraron documentos para guardar en la base de datos.")

    df_verificacion = pd.read_sql('SELECT * FROM tabla_document_collections', engine)
    print("Últimos registros en tabla_document_collections:")
    print(df_verificacion.tail(50))
