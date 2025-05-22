@echo off
cd /d C:\Users\francisco.contreras\Desktop\jupyter-projects\notebooks\MAYA-Modular
call C:\Users\francisco.contreras\Desktop\jupyter-projects\jbpm-data\Scripts\activate.bat

REM Crear carpeta de logs si no existe
if not exist logs mkdir logs

REM Obtener fecha-hora para nombre de archivo
for /f %%i in ('powershell -Command "Get-Date -Format yyyy-MM-dd_HH-mm-ss"') do set LOG_FILE=logs\salida_%%i.log

REM Ejecutar la API redirigiendo stdout y stderr al archivo
python -m app.main >> %LOG_FILE% 2>&1
