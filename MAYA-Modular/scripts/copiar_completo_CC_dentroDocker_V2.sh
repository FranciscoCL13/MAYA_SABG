#!/bin/bash

# Directorios mapeados localmente (por ejemplo, desde Docker Desktop)
SOURCE_DIR="/z/jbpm_docs_mapeo/.docs"
BASE_DEST="/z/jbpm_docs_mapeo/jbpm_docs"
FECHA_ACTUAL=$(date +%F)
DESTINO_FECHA="$BASE_DEST/$FECHA_ACTUAL"

mkdir -p "$DESTINO_FECHA"

echo "[INFO] Fecha actual: $FECHA_ACTUAL"
echo "[INFO] Carpeta destino: $DESTINO_FECHA"
echo "[INFO] Analizando carpetas UUID en .docs..."

for carpeta_uuid in "$SOURCE_DIR"/*/; do
    uuid=$(basename "$carpeta_uuid")

    ya_existe=$(find "$BASE_DEST" -mindepth 2 -maxdepth 2 -type d -name "$uuid")

    if [ -n "$ya_existe" ]; then
        echo "[SKIP] UUID '$uuid' ya fue copiado anteriormente en: $ya_existe"
    else
        echo "[COPY] Copiando UUID '$uuid' a carpeta de hoy..."
        cp -r "$carpeta_uuid" "$DESTINO_FECHA/"
    fi
done

echo "[FIN] Proceso completado."
