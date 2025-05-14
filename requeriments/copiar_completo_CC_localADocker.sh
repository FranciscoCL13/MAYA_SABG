#!/bin/bash

echo "[YY] Copiando SOLO archivos (sin subdirectorios) desde .docs dentro del contenedor..."

# 1. Fecha actual para la subcarpeta destino
FECHA=$(date +%F)
DESTINO="/opt/jboss/wildfly/bin/jbpm_docs/${FECHA}"

# 2. Ejecutar todo dentro del contenedor
docker exec -u 0 jbpm-server bash -c "
    echo '[YY] Creando carpeta destino: $DESTINO'
    mkdir -p \"$DESTINO\"

    echo '[YY] Empaquetando toda la carpeta .docs en un .tar...'
    tar -cvf /tmp/docs_only.tar -C /opt/jboss/wildfly/bin/.docs .
    
    echo '[YY] Moviendo el .tar al destino...'
    mv /tmp/docs_only.tar \"$DESTINO/docs_only.tar\"

    echo '[YY] Descomprimiendo el .tar en el destino...'
    tar -xvf \"$DESTINO/docs_only.tar\" -C \"$DESTINO\"

    echo '[YY] Eliminando el archivo .tar...'
    rm -f \"$DESTINO/docs_only.tar\"

    echo '[YY] ¡Proceso completo!'
"
