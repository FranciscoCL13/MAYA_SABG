from flask import Flask
import subprocess

app = Flask(__name__)


@app.route('/copiar_y_limpiar', methods=['POST'])
def copiar_y_limpiar():
#     subprocess.call(['bash', r'C:\Users\francisco.contreras\Desktop\jupyter-projects\notebooks\requeriments\copiar_completo_CC_localADocker.sh'])
#     subprocess.call(['bash', r'C:\Users\francisco.contreras\Desktop\jupyter-projects\notebooks\requeriments\limpiar_jbpm_docs_localADocker.sh'])
    subprocess.call([r'C:\Program Files\Git\bin\bash.exe', r'C:\Users\francisco.contreras\Desktop\jupyter-projects\notebooks\requeriments\copiar_completo_CC_localADocker.sh'])
    subprocess.call([r'C:\Program Files\Git\bin\bash.exe', r'C:\Users\francisco.contreras\Desktop\jupyter-projects\notebooks\requeriments\limpiar_jbpm_docs_localADocker.sh'])
    return 'OK', 200


if __name__ == '__main__':
    app.run(port=8083)
