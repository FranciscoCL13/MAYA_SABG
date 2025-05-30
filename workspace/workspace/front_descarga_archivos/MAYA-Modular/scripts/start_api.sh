#!/bin/bash

cd "$(dirname "$0")/.."
mkdir -p logs

LOG_FILE="logs/salida_$(date +%Y-%m-%d_%H-%M-%S).log"

# Verifica si hay un archivo api.pid
if [ -f api.pid ]; then
    PID=$(cat api.pid)
    # Verifica si el proceso sigue activo
    if ps -p $PID > /dev/null 2>&1; then
        echo "[INFO] Ya hay una instancia activa de app.main con PID $PID."
        echo "[INFO] Para ver el log en tiempo real, ejecuta:"
        echo "tail -f \$(ls -t ../logs/salida_*.log | head -n 1)"



        
        exit 0
    else
        echo "[INFO] El archivo api.pid existe pero el proceso no está activo. Se iniciará una nueva instancia."
        echo "[INFO] Para ver el log en tiempo real, ejecuta:"
        echo "tail -f \$(ls -t ../logs/salida_*.log | head -n 1)"

        
        rm -f api.pid
    fi
fi

echo "[INFO] No se encontró instancia activa de app.main. Iniciando API..."


nohup python -m app.main >> "$LOG_FILE" 2>&1 &
echo $! > api.pid
echo "[INFO] API iniciada correctamente con PID $(cat api.pid)."
echo "[INFO] Log de ejecución: $LOG_FILE"

