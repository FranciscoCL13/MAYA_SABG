from flask import Flask
import subprocess
import documentCollection  # Asegúrate de que este archivo esté en el mismo directorio o en PYTHONPATH

app = Flask(__name__)

@app.route('/copiar_y_limpiar', methods=['POST'])
def copiar_y_limpiar():
    try:
        subprocess.call([r'C:\Program Files\Git\bin\bash.exe',
                         r'C:\Users\francisco.contreras\Desktop\jupyter-projects\notebooks\requeriments\copiar_completo_CC_localADocker.sh'])
        subprocess.call([r'C:\Program Files\Git\bin\bash.exe',
                         r'C:\Users\francisco.contreras\Desktop\jupyter-projects\notebooks\requeriments\limpiar_jbpm_docs_localADocker.sh'])

        # Ejecutar flujo de extracción y guardado documentCollection.py
        print("-----INICIANDO PROCESO documentCollection---------")
        documentCollection.main()
        print("FINALIZANDO PROCESO documentCollection")
        
        return 'Proceso ejecutado correctamente.', 200

    except Exception as e:
        return f'Error durante la ejecución: {str(e)}', 500

if __name__ == '__main__':
    app.run(port=8083)
