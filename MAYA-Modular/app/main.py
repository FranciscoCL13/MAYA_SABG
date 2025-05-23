from app import create_app
import subprocess
import os


app = create_app()

# Ruta donde están tus scripts
SCRIPT_DIR = os.path.join(os.path.dirname(__file__), '..', 'scripts')

# -----------------------------------------------------------------------
def ejecutar_script(nombre_script):
    ruta_script = os.path.join(SCRIPT_DIR, nombre_script)
    try:
        result = subprocess.run(
            [r'C:\Program Files\Git\bin\bash.exe', ruta_script],
            capture_output=True, text=True
        )
        print(f"[INFO] Salida de {nombre_script}:\n{result.stdout}")
        if result.returncode != 0:
            print(f"[ERROR] Error en {nombre_script}: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"[ERROR] Excepción al ejecutar {nombre_script}: {e}")
        return False
# -----------------------------------------------------------------------

@app.route('/copiar_y_limpiar', methods=['POST'])
def copiar_y_limpiar():
    print(">>> Iniciando ejecución de scripts básicos...")

    if not ejecutar_script('copiar_completo_CC_localADocker_V2.sh'):
        return 'Error ejecutando el script de copia.', 500

    if not ejecutar_script('limpiar_jbpm_docs_localADocker.sh'):
        return 'Error ejecutando el script de limpieza.', 500

    print(">>> Finalizó ejecución de scripts básicos.")
    return 'Scripts ejecutados correctamente.', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8083, debug=True)
