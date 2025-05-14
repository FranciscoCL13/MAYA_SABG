#!/bin/bash

echo "[YY] Copiando SOLO archivos (sin subdirectorios) desde .docs dentro del contenedor..."

# Obtener fecha actual desde tu sistema
ORIGEN="/opt/jboss/wildfly/bin/.docs"
FECHA=$(date +%F)
DESTINO="/opt/jboss/wildfly/bin/jbpm_docs/${FECHA}"


# Ejecutar todos los comandos dentro del contenedor
docker exec -u 0 jbpm-server bash -c "
    echo '[YY] Creando carpeta destino si no existe:'
    mkdir -p "$DESTINO"

    echo '[YY] Copiando solo archivos planos desde .docs a destino'
    find "$ORIGEN" -type f -exec cp {} "$DESTINO" \;

    echo '[YY] ¡Proceso completo!'
"
