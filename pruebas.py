import logging
from app import create_app
from app.functions import extract_and_store_documents

app = create_app()

#Configurar logging para consola
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/copiar_y_limpiar', methods=['POST'])
def copiar_y_limpiar():
    logger.info("--------------INICIANDO PROCESO documentCollection--------------")
    try:
        extract_and_store_documents()
    except Exception as e:
        logger.info(f"[ERROR] Fallo en documentCollection: {e}")
        return 'Error en proceso documentCollection.', 500
    logger.info("--------------FINALIZANDO PROCESO documentCollection------------")

    return 'Proceso ejecutado correctamente.', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8083, debug=True)

--------------------------------------------------------------------------------------

                
