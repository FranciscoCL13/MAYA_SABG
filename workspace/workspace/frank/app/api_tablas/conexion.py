import os

ARCHIVOS_BASE_DIR = os.getenv('ARCHIVOS_BASE_DIR', '/MayaPruebaAdjuntos')

def obtener_documentos():
    documentos = []
    if not os.path.exists(ARCHIVOS_BASE_DIR):
        return documentos

    for document_id in os.listdir(ARCHIVOS_BASE_DIR):
        carpeta = os.path.join(ARCHIVOS_BASE_DIR, document_id)
        if not os.path.isdir(carpeta):
            continue
        for archivo in os.listdir(carpeta):
            ruta_archivo = os.path.join(carpeta, archivo)
            documentos.append({
                "document_id": document_id,
                "archivo": archivo,
                "ruta": ruta_archivo
            })
    return documentos
