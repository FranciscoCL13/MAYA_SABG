#!/bin/bash

echo "[YY]Empaquetando la carpeta .docs completa desde el contenedor, incluyendo subcarpetas..."

# 1. Obtener fecha actual para subcarpeta
FECHA=$(date +%F)
DESTINO="/opt/jboss/wildfly/bin/jbpm_docs/${FECHA}"

# 2. Crear subcarpeta de destino si no existe
mkdir -p "$DESTINO"

# 3. Crear archivo .tar incluyendo toda la estructura
tar -cvf /tmp/docs_only.tar -C /opt/jboss/wildfly/bin/.docs .

# 4. Mover el .tar al destino
mv /tmp/docs_only.tar "$DESTINO/docs_only.tar"

# 5. Descomprimir automáticamente el .tar en el destino
echo "[YY]Descomprimiendo archivo en $DESTINO..."
tar -xvf "$DESTINO/docs_only.tar" -C "$DESTINO"

# 6. Eliminar el .tar después de descomprimir
rm -f "$DESTINO/docs_only.tar"

echo "[YY]¡Proceso completo! Archivos copiados, extraídos y .docs limpiado."