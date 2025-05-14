@echo off
echo Empaquetando la carpeta .docs completa desde el contenedor, incluyendo subcarpetas...

:: 1. Obtener fecha actual para subcarpeta
set FECHA=%date:~6,4%-%date:~3,2%-%date:~0,2%
set DESTINO=Z:\jbpm_docs\%FECHA%

:: 2. Crear subcarpeta de destino si no existe
mkdir "%DESTINO%"

:: 3. Crear archivo .tar dentro del contenedor, incluyendo toda la estructura
docker exec jbpm-server bash -c "tar -cvf /tmp/docs_only.tar -C /opt/jboss/wildfly/bin/.docs ."

:: 4. Copiar el .tar al destino
docker cp jbpm-server:/tmp/docs_only.tar "%DESTINO%\docs_only.tar"

:: 5. Eliminar archivo temporal en el contenedor
docker exec jbpm-server rm -f /tmp/docs_only.tar


:: 7. Descomprimir automáticamente el .tar en el destino
echo Descomprimiendo archivo en %DESTINO%...
tar -xvf "%DESTINO%\docs_only.tar" -C "%DESTINO%"

:: 8. Eliminar el .tar después de descomprimir
del "%DESTINO%\docs_only.tar"

echo ¡Proceso completo! Archivos copiados, extraídos y .docs limpiado.
