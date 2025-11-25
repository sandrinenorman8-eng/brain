@echo off
echo ========================================
echo  Protocole de Test d'Integre - Deuxieme Cerveau
echo  Execution Automatisee (Robot)
echo ========================================
echo.

echo [INFO] Verification des prerequis...
echo.

REM Verifier si PowerShell est disponible
powershell -Command "Write-Host 'PowerShell OK'" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] PowerShell n'est pas disponible sur ce systeme
    echo [INFO] Installez PowerShell pour executer les tests
    pause
    exit /b 1
)

echo [INFO] PowerShell detecte
echo.

REM Verifier si le serveur Flask est en cours d'execution
echo [INFO] Verification du serveur Flask...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:5008' -TimeoutSec 5; exit 0 } catch { exit 1 }" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Le serveur Flask n'est pas accessible sur http://localhost:5008
    echo [INFO] Demarrez d'abord le serveur avec: python app.py
    echo.
    echo [INFO] Voulez-vous demarrer le serveur maintenant? (O/N)
    set /p choix=
    if /i "%choix%"=="O" (
        echo [INFO] Demarrage du serveur Flask...
        start cmd /c "python app.py"
        timeout /t 3 >nul
    ) else (
        echo [INFO] Annulation des tests
        pause
        exit /b 1
    )
)

echo [INFO] Serveur Flask accessible
echo.

REM Executer les tests avec timeout de securite
echo [INFO] Execution des tests d'integrite...
echo [INFO] Timeout maximum: 300 secondes (5 minutes)
echo.

powershell -ExecutionPolicy Bypass -File "test_integration_protocol.ps1"

echo.
echo [INFO] Tests termines. Consultez le rapport genere.
echo.

REM Lister les rapports generes
echo [INFO] Rapports disponibles:
dir test_report_*.log /b 2>nul
if errorlevel 1 (
    echo Aucun rapport trouve
)

echo.
pause
