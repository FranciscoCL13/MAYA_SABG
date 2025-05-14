@echo off
echo Empaquetando todos los archivos desde el contenedor...

docker exec jbpm-server bash -c "mkdir -p /tmp/docs_flat && find /opt/jboss/wildfly/bin/.docs/ -type f -exec cp {} /tmp/docs_flat/ \;"

docker exec jbpm-server bash -c "tar -cvf /tmp/docs_only.tar -C /tmp/docs_flat ."

docker cp jbpm-server:/tmp/docs_only.tar "C:\Users\francisco.contreras\Desktop\jupyter-projects\notebooks\archivosAdjuntos\docs_only.tar"

docker exec jbpm-server rm -rf /tmp/docs_flat /tmp/docs_only.tar

echo Listo. Ahora puedes descomprimir el archivo .tar en tu carpeta destino.

