## Como acceder:
0. python -m app.main ó nohup python -m app.main > salida.log 2>&1 & (Segundo plano)
1. La raíz de tu API de tablas será:
http://localhost:8083/tablas/
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

## TODO COMO ROOT USER

## INSTALAR PYTHON3 - actualizar CENTOS
dar permisos a internet:
ping -c 3 8.8.8.8        # Verifica si tienes conexión IP
ping -c 3 google.com     # Verifica si puedes resolver DNS

entrar exect -it... jbpm-server

editar archivo: vi /etc/yum.repos.d/CentOS-Base.repo

instalar:
yum clean all
yum makecache
yum install -y python3
python3 -m pip install --user flask
python3 -m pip install flask

## CREAR ENTORNO VIrtuAL dentro de Docker

python3 -m venv /opt/myenv
source /opt/myenv/bin/activate
pip install flask
yum install -y postgresql-devel
pip install --upgrade pip
yum groupinstall -y "Development Tools"
yum install -y python3-devel
yum install python3-devel
pip install sqlalchemy


pip install -r requirements.txt

## VER LOGS DE SALIDA ESTANDO EN CARPETA LOGS
tail -f \$(ls -t logs/salida_*.log | head -n 1)