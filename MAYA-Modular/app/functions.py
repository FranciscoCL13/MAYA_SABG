import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
from sqlalchemy import inspect
from app.conexion import get_engine

# ================================
# Parámetros de conexión jBPM
# ================================
JBPM_HOST = "http://host.docker.internal:8080"
USERNAME = "wbadmin"
PASSWORD = "wbadmin"
CONTAINER_ID = "Publica_In_Out_1.0.0-SNAPSHOT"
HEADERS = {"Accept": "application/json"}
AUTH = HTTPBasicAuth(USERNAME, PASSWORD)

# ================================
# Obtener último processInstanceId
# ================================
def get_latest_process_instance():
    url = f"{JBPM_HOST}/kie-server/services/rest/server/queries/processes/instances?status=1&page=0&pageSize=10"
    print(f"[INFO] Consultando últimas instancias activas en: {url}")
    try:
        response = requests.get(url, headers=HEADERS, auth=AUTH, timeout=10)
        response.raise_for_status()
        instances = response.json().get("process-instance", [])
        if not instances:
            print("[INFO] No hay instancias activas.")
            return None
        latest = instances[0]
        print(f"[OK] Última instancia activa: {latest.get('process-instance-id')}")
        return latest.get("process-instance-id")
    except Exception as e:
        print(f"[ERROR] Fallo en get_latest_process_instance: {e}")
        return None

# ================================
# Obtener todos los documentos del proceso
# ================================
def get_all_documents(process_instance_id):
    url = f"{JBPM_HOST}/kie-server/services/rest/server/containers/{CONTAINER_ID}/processes/instances/{process_instance_id}/variables"
    print(f"[INFO] Consultando variables del proceso: {url}")
    try:
        response = requests.get(url, headers=HEADERS, auth=AUTH)
        print(f"[DEBUG] Código de respuesta: {response.status_code}")
        print(f"[DEBUG] Respuesta raw: {response.text}")

        response.raise_for_status()
        data = response.json()
        print(f"[DEBUG] Variables encontradas: {list(data.keys())}")

        resultados = []

        for var_name, var_value in data.items():
            print(f"[DEBUG] Analizando variable: {var_name}")
            if isinstance(var_value, dict) and "documents" in var_value:
                print(f"[DEBUG] Se encontraron documentos en {var_name}")
                for doc in var_value["documents"]:
                    doc_data = doc.get("org.jbpm.document.service.impl.DocumentImpl", {})
                    resultados.append({
                        "processinstanceid": process_instance_id,
                        "value": f"{doc_data.get('name', 'sin_nombre')}####{doc_data.get('identifier', 'sin_id')}",
                        "lastModified": doc_data.get("lastModified", {}).get("java.util.Date", None),
                        "variable": var_name,
                        "identifier": doc_data.get("identifier", "sin_id")
                    })
            else:
                print(f"[DEBUG] {var_name} no contiene documentos")

        if not resultados:
            print("[WARN] No se encontraron documentos.")

        return resultados

    except Exception as e:
        print(f"[ERROR] Fallo en get_all_documents: {e}")
        return []


# ================================
# Ejecutar y almacenar documentos
# ================================
def extract_and_store_documents():
    try:
        print("-----INICIANDO PROCESO documentCollection---------")

        process_instance_id = get_latest_process_instance()
        print(f"[ZZ] Instancia obtenida: {process_instance_id}")

        if not process_instance_id:
            print("[INFO] No se pudo continuar sin instancia activa.")
            return

        docs = get_all_documents(process_instance_id)
        if not docs:
            print("[INFO] No se encontraron documentos para procesar.")
            return

        dfCollect = pd.DataFrame(docs)
        engine = get_engine()

        with engine.connect() as conn:
            inspector = inspect(engine)
            tables = inspector.get_table_names()

            if 'tabla_document_collections' not in tables:
                dfCollect.to_sql('tabla_document_collections', con=engine, if_exists='replace', index=False)
                print("[OK] Tabla creada e información insertada.")
            else:
                existing_ids = pd.read_sql('SELECT identifier FROM tabla_document_collections', con=engine)['identifier'].astype(str)
                df_nuevos = dfCollect[~dfCollect['identifier'].astype(str).isin(existing_ids)]
                if not df_nuevos.empty:
                    df_nuevos.to_sql('tabla_document_collections', con=engine, if_exists='append', index=False)
                    print(f"[OK] Se insertaron {len(df_nuevos)} documento(s) nuevo(s).")
                else:
                    print("[INFO] No hay nuevos documentos para insertar.")

        df_verificacion = pd.read_sql('SELECT * FROM tabla_document_collections', engine)
        print("[INFO] Últimos registros en tabla_document_collections:")
        print(df_verificacion)

    except Exception as e:
        print(f"[ERROR] Fallo inesperado en extract_and_store_documents: {e}")
