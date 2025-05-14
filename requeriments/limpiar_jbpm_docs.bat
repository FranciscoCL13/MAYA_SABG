@echo off
setlocal EnableDelayedExpansion

:: Ruta de la carpeta compartida desde Docker (por ejemplo, montada como Z:)
set "DIR=/opt/jboss/wildfly/bin/.docs"

:: Tamaño máximo permitido en bytes
set MAX_SIZE=6665555

:: Verificar si la carpeta existe
if not exist "%DIR%" (
    echo La carpeta %DIR% no existe.
    exit /b 1
)

:: Calcular el tamaño total usando PowerShell
set TOTAL_SIZE=0
for /f %%A in ('powershell -command "(Get-ChildItem -Recurse -Force '%DIR%' | Measure-Object Length -Sum).Sum"') do (
    set TOTAL_SIZE=%%A
)

echo Tamanio actual de %DIR%: %TOTAL_SIZE% bytes
echo Limite configurado: %MAX_SIZE% bytes

:: Comparar tamaños
set /a COMPARE=!TOTAL_SIZE! - %MAX_SIZE%
if !COMPARE! gtr 0 (
    echo Supera el límite. Eliminando contenido...
    
    :: Eliminar archivos
    for /f %%F in ('dir /b /a:-d "%DIR%"') do (
        del /q /f "%DIR%\%%F"
    )

    :: Eliminar carpetas
    for /d %%D in ("%DIR%\*") do (
        rd /s /q "%%D"
    )

    echo Contenido de %DIR% eliminado.
) else (
    echo Dentro del limite. No se borra nada.
)
