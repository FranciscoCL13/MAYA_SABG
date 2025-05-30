#!/bin/bash

# Ruta de la carpeta de documentos
DIR="/opt/jboss/wildfly/bin/.docs"

# Tamaño máximo permitido en bytes (100 GB)
MAX_SIZE=90737

# Verifica si la carpeta existe
if [ ! -d "$DIR" ]; then
    echo "La carpeta $DIR no existe."
    exit 1
fi

# Calcular tamaño total de la carpeta en bytes
TOTAL_SIZE=$(du -sb "$DIR" | awk '{print $1}')

echo "[YY]Tamaño actual de $DIR: $TOTAL_SIZE bytes"
echo "[YY]Límite configurado: $MAX_SIZE bytes"

# Comparar con el límite
if [ "$TOTAL_SIZE" -gt "$MAX_SIZE" ]; then
    echo "[YY]Supera el límite. Eliminando archivos dentro de los subdirectorios..."
    find "$DIR" -type f -exec rm -f {} \; #-type f selecciona solo archivos (files).
    echo "[YY]Archivos eliminados. Directorios preservados."
else
    echo "[YY]Dentro del límite. No se borra nada."
fi