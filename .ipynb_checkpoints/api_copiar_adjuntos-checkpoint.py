# Importamos los módulos necesarios
from flask import Flask, request, jsonify  # Flask para crear la API, request para manejar solicitudes y jsonify para responder en formato JSON
import subprocess  # Para ejecutar scripts o comandos del sistema desde Python
import tarfile     # Para manejar archivos comprimidos en formato .tar
import os          # Para trabajar con rutas y verificar existencia de archivos
import subprocess

# Inicializamos la aplicación Flask
app = Flask(__name__)

# ------------------------------------------
# Constantes con las rutas locales del host
# ------------------------------------------

# Ruta absoluta al archivo .bat que copia los archivos desde el contenedor Docker hacia el host
BAT_PATH = r"C:\Users\francisco.contreras\Desktop\jupyter-projects\notebooks\requeriments\copiar_completo.bat"

# Ruta absoluta al archivo .tar generado dentro del contenedor y copiado al host
TAR_PATH = r"C:\Users\francisco.contreras\Desktop\jupyter-projects\notebooks\archivosAdjuntos\docs_only.tar"

# Ruta del directorio donde se extraerán los archivos .tar
EXTRACT_PATH = r"C:\Users\francisco.contreras\Desktop\jupyter-projects\notebooks\archivosAdjuntos"

# Ruta absoluta al script de limpieza .sh que se ejecuta dentro del contenedor
# Este script debe estar montado dentro del contenedor si la API corre ahí
# SCRIPT_LIMPIEZA_PATH = "/opt/jboss/wildfly/bin/limpiar_docs.sh"
SCRIPT_LIMPIEZA_PATH = r"C:\Users\francisco.contreras\Desktop\jupyter-projects\notebooks\requeriments\limpiar_jbpm_docs.bat"

# Nombre del contenedor y ruta del script
# container_name = "jbpm-server"
# script_path = "/opt/jboss/wildfly/bin/limpiar_jbpm_docs.bat"


        


#Si se encuentra en el mismo contenedor
# script_path = "/opt/jboss/wildfly/bin/limpiar_docs.sh"

# result = subprocess.run(["bash", script_path], capture_output=True, text=True)

# print("STDOUT:", result.stdout)
# print("STDERR:", result.stderr)


# -------------------------------------------------
# Ruta de la API: POST /copiar_adjuntos
# Este endpoint es llamado por jBPM u otros sistemas
# -------------------------------------------------
@app.route('/copiar_adjuntos', methods=['POST'])
def copiar_adjuntos():
    try:
        # Ejecutamos el archivo .bat que:
        # 1. Empaqueta los archivos PDF dentro del contenedor Docker
        # 2. Copia el .tar desde el contenedor al host
        # 3. Limpia archivos temporales del contenedor
        print("=== Ejecutando COPIADO de archivos ===")
        result = subprocess.run(BAT_PATH, shell=True)
        print("=== Proceso Finalizado ===")

        # Imprimimos la salida estándar del script
        print("Salida del script de copiar:")
        print(result.stdout)

        # Si hubo errores, también los mostramos (aunque no interrumpan la ejecución)
        if result.stderr:
            print("Errores del script:")
            print(result.stderr)

        # Validamos que el archivo .tar realmente se haya generado y exista
        if not os.path.exists(TAR_PATH):
            return jsonify({"error": "Archivo .tar no encontrado"}), 404

        # Si existe, lo abrimos y extraemos todo su contenido en la carpeta indicada
        print("Descomprimiendo archivo .tar...")
        with tarfile.open(TAR_PATH, "r") as tar:
            tar.extractall(path=EXTRACT_PATH)

        print("¡Archivos extraidos correctamente!")

                    #----------------Limpieza archivos-------------------
        # Comando para ejecutar el sh de limpieza dentro del contenedor
        print("=== Ejecutando MANTENIMIENTO de archivos ===")
        cmd = ["docker", "exec", container_name, "bash", SCRIPT_LIMPIEZA_PATH]
        print("=== Proceso Finalizado ===")
        # Ejecutar y capturar salida
        # result = subprocess.run(cmd, capture_output=True, text=True)
        result = subprocess.run(f'"{script_path}"', shell=True, capture_output=True, text=True)
        # Imprimir salida
        print("STDOUT de mantenimiento:", result.stdout)
        print("STDERR de mantenimiento:", result.stderr)
                    #----------------Limpieza archivos-------------------
        

        # Respondemos con un mensaje JSON indicando éxito
        return jsonify({"mensaje": "Archivos copiados, extraídos y limpieza ejecutada correctamente"}), 200

    # Captura de errores al ejecutar el script .bat
    except subprocess.CalledProcessError as e:
        return jsonify({
            "error": "Error al ejecutar el script",
            "detalle": e.stderr
        }), 500

    # Captura de cualquier otro error inesperado
    except Exception as ex:
        return jsonify({
            "error": "Excepción general al procesar la solicitud",
            "detalle": str(ex)
        }), 500

# -------------------------------------------------------------
# Punto de entrada principal de la aplicación Flask
# Se expone por todas las interfaces (host=0.0.0.0) en el puerto 8083
# -------------------------------------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8083, debug=False)
