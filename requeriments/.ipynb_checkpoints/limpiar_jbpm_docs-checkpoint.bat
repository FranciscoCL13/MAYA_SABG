@echo off
setlocal EnableDelayedExpansion

:: Ruta de la carpeta (usar doble backslash o comillas si tiene espacios)
set "DIR=C:\ruta\al\directorio\.docs"

:: Tamaño máximo permitido (en bytes)
set MAX_SIZE=666555

:: Verificar si la carpeta existe
if not exist "%DIR%" (
    echo La carpeta %DIR% no existe.
    exit /b 1
)

:: Calcular el tamaño total de la carpeta (en bytes)
set TOTAL_SIZE=0
for /f "usebackq" %%A in (`powershell -command "(Get-ChildItem -Recurse -Force '%DIR%' | Measure-Object -Property Length -Sum).Sum"`) do (
    set TOTAL_SIZE=%%A
)

echo Tamaño actual de %DIR%: %TOTAL_SIZE% bytes
echo Límite configurado: %MAX_SIZE% bytes

:: Comparar tamaños
set /a COMPARE=!TOTAL_SIZE! - %MAX_SIZE%
if !COMPARE! gtr 0 (
    echo Supera el límite. Eliminando contenido...
    del /q /f "%DIR%\*.*"
    for /d %%D in ("%DIR%\*") do rd /s /q "%%D"
    echo Contenido de %DIR% eliminado.
) else (
    echo Dentro del límite. No se borra nada.
)
