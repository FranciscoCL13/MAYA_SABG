import os

class Config:
    # Clave para sesiones seguras
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')

    # Rutas de archivos
    ARCHIVOS_BASE_DIR = os.getenv('ARCHIVOS_BASE_DIR', '/MayaPruebaAdjuntos')
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', os.path.join(os.path.dirname(__file__), 'uploaded_docs'))

    # jBPM
    KIE_SERVER_URL = os.getenv('KIE_SERVER_URL', 'http://172.25.30.98:8080/kie-server/services/rest/server')
    KIE_USERNAME = os.getenv('KIE_USERNAME', 'wbadmin')
    KIE_PASSWORD = os.getenv('KIE_PASSWORD', 'wbadmin')

    # CORS
    CORS_ORIGINS = ["http://172.25.30.98:8083", "http://localhost:8080"]

    # Procesos disponibles (para e.firma)
    CONFIG_PROCESOS = {
        "Público": {
            "containerId": "Publica_In_Out_1.0.0-SNAPSHOT",
            "processId": "Publica_In_Out.Publica"
        },
        "Privado": {
            "containerId": "Privada_1.0.0-SNAPSHOT",
            "processId": "Privada.Privada_In_Out"
        },
        "Social": {
            "containerId": "Social_In_Out_1.0.0-SNAPSHOT",
            "processId": "Social_In_Out.Social"
        }
    }
