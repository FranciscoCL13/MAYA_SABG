#!/bin/bash
# Script para limpiar archivos temporales o no deseados en el directorio

DIR="/ruta/destino"

echo "Limpiando archivos en $DIR ..."
rm -rf "$DIR"/temp_*
echo "Limpieza completada."
