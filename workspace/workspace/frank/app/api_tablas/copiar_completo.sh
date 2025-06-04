#!/bin/bash
# Script para copiar archivos completos desde la fuente a destino

SRC="/ruta/origen"
DST="/ruta/destino"

echo "Copiando archivos de $SRC a $DST ..."
cp -r "$SRC"/* "$DST"/
echo "Copia completada."
