from app import create_app
import subprocess
import os
from app.functions import extract_and_store_documents
from app.conexion import get_engine


app = create_app()

# Ruta scripts bash
SCRIPT_DIR = os.path.join(os.path.dirname(__file__), '..', 'scripts')

@app.route('/copiar_y_limpiar', methods=['POST'])
def copiar_y_limpiar():
    try:
        subprocess.call([
            r'C:\Program Files\Git\bin\bash.exe',
            os.path.join(SCRIPT_DIR, 'copiar_completo_CC_localADocker.sh')
        ])
        subprocess.call([
            r'C:\Program Files\Git\bin\bash.exe',
            os.path.join(SCRIPT_DIR, 'limpiar_jbpm_docs_localADocker.sh')
        ])

        print("-----INICIANDO PROCESO documentCollection---------")
        extract_and_store_documents()
        print("FINALIZANDO PROCESO documentCollection")

        return 'Proceso ejecutado correctamente.', 200

    except Exception as e:
        return f'Error durante la ejecución: {str(e)}', 500

if __name__ == '__main__':
    app.run(port=8083, debug=True)
