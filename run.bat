@echo off
REM 

echo ========================================
echo    Device Finder - Localizador
echo ========================================
echo.

REM 
py --version >nul 2>&1
if errorlevel 1 (
    REM 
    python --version >nul 2>&1
    if errorlevel 1 (
        echo [ERRO] Python nao encontrado!
        echo Por favor, instale Python 3.7 ou superior
        echo Visite: https://www.python.org/downloads/
        pause
        exit /b 1
    )
    set PYTHON_CMD=python
) else (
    set PYTHON_CMD=py
)

echo [OK] Python encontrado: %PYTHON_CMD%
echo.

REM 
echo Verificando dependencias...
%PYTHON_CMD% -m pip install -r requirements.txt >nul 2>&1

REM 
echo.
echo Iniciando Device Finder...
echo.
%PYTHON_CMD% __init__.py

pause
