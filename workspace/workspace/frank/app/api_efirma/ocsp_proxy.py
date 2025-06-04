import requests

def validar_ocsp(certificado_base64: str) -> dict:
    """
    Función para validar el certificado mediante OCSP.
    En este ejemplo se simula la validación y se devuelve un resultado ficticio.
    """

    # Aquí se integraría la lógica real para validar OCSP,
    # por ejemplo enviando el certificado a un servidor OCSP y leyendo respuesta.

    # Ejemplo simulado:
    resultado = {
        "estado": "good",   # good, revoked, unknown
        "mensaje": "Certificado válido según OCSP",
    }

    # Si se requiere lógica real, implementar aquí

    return resultado
