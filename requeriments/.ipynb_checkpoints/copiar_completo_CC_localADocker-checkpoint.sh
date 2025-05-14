#!/bin/bash

echo "[YY] Copiando SOLO archivos subidos HOY (con subdirectorios) desde .docs dentro del contenedor..."

# Fecha actual
FECHA=$(date +%F)
DESTINO="/opt/jboss/wildfly/bin/jbpm_docs/${FECHA}"

# Ejecutar dentro del contenedor
docker exec -u 0 jbpm-server bash -c "
    echo '[YY] Creando carpeta destino: $DESTINO'
    mkdir -p \"$DESTINO\"

    cd /opt/jboss/wildfly/bin/.docs

    echo '[YY] Buscando archivos subidos hoy...'
    find . -type f -newerct \"$(date +%F) 00:00:00\" > /tmp/lista_docs_hoy.txt

    CANTIDAD=\$(wc -l < /tmp/lista_docs_hoy.txt)

    if [ \$CANTIDAD -gt 0 ]; then
        echo '[YY] Se encontraron '\$CANTIDAD' archivos subidos hoy.'

        echo '[YY] Empaquetando en un .tar...'
        tar -cvf /tmp/docs_only.tar -T /tmp/lista_docs_hoy.txt

        echo '[YY] Moviendo el .tar al destino...'
        mv /tmp/docs_only.tar \"$DESTINO/docs_only.tar\"

        echo '[YY] Descomprimiendo el .tar en el destino...'
        tar -xvf \"$DESTINO/docs_only.tar\" -C \"$DESTINO\"

        echo '[YY] Limpiando archivos temporales...'
        rm -f \"$DESTINO/docs_only.tar\" /tmp/lista_docs_hoy.txt
    else
        echo '[YY] No hay archivos subidos HOY. Nada que copiar.'
    fi

    echo '[YY] Total de archivos copiados hoy: '\$CANTIDAD
    echo '[YY] ¡Proceso completo!'
"
