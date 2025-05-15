#!/bin/bash

# Nombre del contenedor
CONTAINER_NAME="jbpm-server"

# Ruta de la carpeta dentro del contenedor
DIR="/opt/jboss/wildfly/bin/.docs"

# Tamaño máximo permitido en bytes (100 GB)
MAX_SIZE=107374182400

echo "[YY]Verificando existencia y tamaño de $DIR dentro del contenedor '$CONTAINER_NAME'..."

# Ejecutar dentro del contenedor
docker exec -u 0 "$CONTAINER_NAME" bash -c "
  if [ ! -d \"$DIR\" ]; then
      echo '[YY]La carpeta $DIR no existe.'
      exit 1
  fi

  TOTAL_SIZE=\$(du -sb \"$DIR\" | awk '{print \$1}')
  echo '[YY]Tamaño actual de $DIR: '\$TOTAL_SIZE' bytes'
  echo '[YY]Límite configurado: $MAX_SIZE bytes'

  if [ \"\$TOTAL_SIZE\" -gt \"$MAX_SIZE\" ]; then
      echo '[YY]Supera el límite. Eliminando archivos dentro de los subdirectorios...'
      find \"$DIR\" -type f -exec rm -f {} \;
      echo '[YY]Archivos eliminados. Directorios preservados.'
  else
      echo '[YY]Dentro del límite. No se borra nada.'
  fi
"
