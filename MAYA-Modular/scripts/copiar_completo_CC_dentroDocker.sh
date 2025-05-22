#!/bin/bash

echo "[CHECK] Copiando SOLO carpetas UUID nuevas desde .docs al día actual (evitando duplicados previos)..."

FECHA=$(date +%F)
BASE="/opt/jboss/wildfly/bin/"
BASEDEST="/opt/jboss/wildfly/bin/jbpm_docs/"
DESTINO="${BASEDEST}/${FECHA}"

echo "[CHECK] Creando carpeta destino si no existe: $DESTINO"
mkdir -p "$DESTINO"

cd "${BASE}/.docs" || { echo "No existe carpeta .docs"; exit 1; }

echo "[CHECK] Iniciando recorrido de carpetas UUID en .docs..."
for uuid_dir in */; do
    uuid=${uuid_dir%/}

    encontrado=$(find "${BASE}/jbpm_docs/" -mindepth 2 -maxdepth 2 -type d -name "$uuid")

    if [ -n "$encontrado" ]; then
        echo "[SKIP] UUID '$uuid' ya existe en: $encontrado"
    else
        echo "[COPY] Copiando '$uuid' a carpeta de hoy..."
        cp -r "${BASE}/.docs/$uuid" "$DESTINO/"
    fi
done

echo "[CHECK] ¡Proceso completado!"
