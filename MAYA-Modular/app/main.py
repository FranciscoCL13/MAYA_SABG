from app import create_app
import subprocess
import os
from app.functions import extract_and_store_documents

app = create_app()
SCRIPT_DIR = os.path.join(os.path.dirname(__file__), '..', 'scripts')

def ejecutar_script(script_name):
    ruta_script = os.path.join(SCRIPT_DIR, script_name)
    try:
        result = subprocess.run(
            [r'C:\Program Files\Git\bin\bash.exe', ruta_script],
            capture_output=True, text=True
        )
        print(f"[INFO] Salida {script_name}:\n{result.stdout}")
        if result.returncode != 0:
            print(f"[ERROR] Fallo en {script_name}: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"[ERROR] Excepción al ejecutar {script_name}: {e}")
        return False

@app.route('/copiar_y_limpiar', methods=['POST'])
def copiar_y_limpiar():
    if not ejecutar_script('copiar_completo_CC_localADocker.sh'):
        return 'Error en script de copia.', 500
    if not ejecutar_script('limpiar_jbpm_docs_localADocker.sh'):
        return 'Error en script de limpieza.', 500

    print("-----INICIANDO PROCESO documentCollection---------")
    extract_and_store_documents()
    print("FINALIZANDO PROCESO documentCollection")

    return 'Proceso ejecutado correctamente.', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8083, debug=True)

