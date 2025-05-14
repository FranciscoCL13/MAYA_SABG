#!/bin/bash

echo "[YY]Copiando SOLO archivos (sin subdirectorios) desde .docs..."

# 1. Fecha actual para subcarpeta de destino
ORIGEN="/opt/jboss/wildfly/bin/.docs"
FECHA=$(date +%F)
DESTINO="/opt/jboss/wildfly/bin/jbpm_docs/${FECHA}"

# Crear carpeta destino si no existe
mkdir -p "$DESTINO"

# Buscar todos los archivos dentro de .docs y copiarlos al destino sin las carpetas
find "$ORIGEN" -type f -exec cp {} "$DESTINO" \;

echo "[YY]¡Proceso completo! Archivos copiados a: $DESTINO"