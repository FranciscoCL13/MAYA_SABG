from flask import Flask, request, render_template, jsonify
import requests
import base64

app = Flask(__name__)

KIE_SERVER_URL = "http://172.25.30.94:8080/kie-server/services/rest/server"
CONTAINER_ID = "Publica_In_Out_1.0.0-SNAPSHOT"
PROCESS_ID = "Publica_In_Out.Publica"
KIE_USERNAME = "wbadmin"
KIE_PASSWORD = "wbadmin"

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Recibe datos del formulario
    var1 = request.form.get('variable1')
    var2 = request.form.get('variable2')

    # Prepara la autenticación en base64
    credentials = f"{KIE_USERNAME}:{KIE_PASSWORD}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {encoded_credentials}"
    }

    # Construye el cuerpo con las variables del proceso
    payload = {
        "variable_del_proceso1": var1,
        "variable_del_proceso2": var2
    }

    # Construye la URL completa
    url = f"{KIE_SERVER_URL}/containers/{CONTAINER_ID}/processes/{PROCESS_ID}/instances"

    # Hace la solicitud POST a jBPM
    response = requests.post(url, headers=headers, json=payload)

    # Devuelve respuesta legible
    if response.status_code == 201:
        return f"Proceso iniciado correctamente. ID: {response.text}"
    else:
        return f"Error al iniciar el proceso: {response.status_code} - {response.text}", response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

