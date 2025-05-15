## Como acceder:
0. python -m app.main
1. La raíz de tu API de tablas será:
http://localhost:5000/tablas/
http://127.0.0.1:8083/tablas/

2. Endpoint para descargar archivos:
http://localhost:5000/tablas_busqueda/descargar/<filename>

3. Endpoint para generar la tabla:
http://localhost:5000/tablas_busqueda/generar_tabla

4. FLASK corre:
http://127.0.0.1:8083

# Extracción y Almacenamiento de Documentos desde jBPM

Este proyecto contiene una API Flask que ejecuta un flujo completo para:

1. Copiar y limpiar archivos desde rutas compartidas.
2. Extraer documentos desde variables de proceso en jBPM.
3. Almacenar información en una base de datos PostgreSQL.

---

## 📁 Estructura del Proyecto
MAYA/
    ├── app/
    │ ├── main.py # API Flask
    │ ├── conexion.py # Conexión a PostgreSQL
    │ ├── tablas_busqueda.py
    │ ├── __init__.py
    │ └── functions.py # Funciones de extracción y guardado
    ├── scripts/
    │ ├── copiar_completo_CC_localADocker.sh
    │ └── limpiar_jbpm_docs_localADocker.sh
    ├── requirements.txt
    └── README.md


## FINAL - EJECUTAR un proceso en JBPM
## Checar BD contendrá
1. Tabla "tabla_document_collections"
2. Copia de archivos adjuntos en "/opt/jboss/wildfly/bin/jbpm_docs/${FECHA}"
3. Mantenimiento (Borrado total a los 100GB de almacenamiento) de carpeta  original en JBPM que contiene los archivos adjuntos


