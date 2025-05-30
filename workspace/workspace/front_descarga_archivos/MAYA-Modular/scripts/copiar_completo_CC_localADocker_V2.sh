#!/bin/bash

echo "[CHECK] Copiando SOLO carpetas UUID nuevas desde .docs al día actual (evitando duplicados previos)..."

# Fecha actual
FECHA=$(date +%F)
DESTINO="/opt/jboss/wildfly/bin/jbpm_docs/${FECHA}"

# Ejecutar dentro del contenedor
docker exec -u 0 jbpm-server bash -c "
    echo '[CHECK] Creando carpeta destino si no existe: $DESTINO'
    mkdir -p \"$DESTINO\"

    cd /opt/jboss/wildfly/bin/.docs || exit 1

    echo '[CHECK] Iniciando recorrido de carpetas UUID en .docs...'
    for uuid_dir in */; do
        uuid=\${uuid_dir%/}

        # Buscar si ya existe en alguna fecha anterior
        encontrado=\$(find /opt/jboss/wildfly/bin/jbpm_docs/ -mindepth 2 -maxdepth 2 -type d -name \"\$uuid\")

        if [ -n \"\$encontrado\" ]; then
            echo \"[SKIP] UUID '\$uuid' ya existe en: \$encontrado\"
        else
            echo \"[COPY] Copiando '\$uuid' a carpeta de hoy...\"
            cp -r \"/opt/jboss/wildfly/bin/.docs/\$uuid\" \"$DESTINO/\"
        fi
    done

    echo '[CHECK] ¡Proceso completado!'
"
