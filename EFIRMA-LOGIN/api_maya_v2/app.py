from flask import Flask, session, request, jsonify, render_template
from pycfdi_credentials import Certificate
import secrets, time, base64
from ocsp_proxy import validar_ocsp_proxy

app = Flask(__name__)
app.secret_key = secrets.token_hex(32) 

@app.route("/", methods=['GET'])
def mostrar_index():
    return render_template("efirma.html")

@app.route("/bienvenido.html")
def bienvenido():
    if 'rfc' not in session:
        return "Acceso no autorizado", 403
    return render_template("bienvenido.html")

@app.route("/", methods=['POST'])
def login():
    data = request.get_json()

    if data and data.get("salir"):
        session.clear()

    elif 'rfc' not in session and 'challenge' in session and all(k in data for k in ['certificado', 'firma_cadena', 'timestamp']) and abs(time.time() - int(data['timestamp'])) <= 300:
        
        try:
            cert = Certificate(base64.b64decode(data['certificado']))
            if cert.verify(base64.b64decode(data['firma_cadena']), (f"{data['timestamp']}_{session['challenge']}").encode("utf-8"), "sha256"):
                ocsp_result = validar_ocsp_proxy(cert.to_pem().decode())

                print("Respuesta OCSP del SAT:", ocsp_result)

                if ocsp_result.get("resultado") == "VALIDO":
                    session['rfc'] = cert.subject.rfc
                else:
                    return jsonify({
                        "error": "Certificado no válido",
                        "detalle": ocsp_result.get("errorMessage", "Certificado inactivo o revocado")
        }), 400
        except Exception as e:
            return jsonify({"error": "Validación fallida", "detalle": str(e)}), 400
    
    if 'rfc' not in session:
        session['challenge'] = secrets.token_hex(4)

    return jsonify(dict(session))





