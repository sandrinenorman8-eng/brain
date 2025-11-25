@echo off
echo ========================================
echo  Deuxieme Cerveau - Structure Organisee
echo  Version 2.0
echo ========================================
echo.

echo [INFO] Verification de PowerShell...
powershell -Command "Write-Host 'PowerShell OK'" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] PowerShell n'est pas disponible
    echo [INFO] Installez PowerShell pour continuer
    pause
    exit /b 1
)

echo [INFO] Demarrage du Deuxieme Cerveau...
echo.

REM Lancer le script PowerShell principal
powershell -ExecutionPolicy Bypass -File "start_deuxieme_cerveau.ps1"

echo.
echo [INFO] Deuxieme Cerveau arrete.
pause

