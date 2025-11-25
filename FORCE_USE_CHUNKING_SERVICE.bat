@echo off
echo ========================================
echo   FORCER UTILISATION CHUNKING SERVICE
echo ========================================
echo.
echo Ce script force l'utilisation du chunking service
echo pour tous les fichiers volumineux (>200 lignes)
echo.
echo ========================================
echo.

REM 1. Vérifier que chunking service tourne
echo [1/3] Verification Chunking Service (port 5009)...
netstat -an | findstr ":5009" >nul
if errorlevel 1 (
    echo [WARN] Chunking Service non detecte
    echo [ACTION] Demarrage automatique...
    start "Chunking Service" cmd /k "cd /d %~dp0deuxieme_cerveau && python chunking_service.py"
    timeout /t 5 /nobreak >nul
) else (
    echo [OK] Chunking Service detecte
)

REM 2. Vérifier Flask Main
echo.
echo [2/3] Verification Flask Main (port 5008)...
netstat -an | findstr ":5008" >nul
if errorlevel 1 (
    echo [WARN] Flask Main non detecte
    echo [ACTION] Lancer START_ALL_SERVICES.bat d'abord
    pause
    exit /b 1
) else (
    echo [OK] Flask Main detecte
)

REM 3. Test rapide
echo.
echo [3/3] Test connexion chunking service...
curl -s http://localhost:5009/health >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Chunking service ne repond pas
    pause
    exit /b 1
) else (
    echo [OK] Chunking service operationnel
)

echo.
echo ========================================
echo   CONFIGURATION ACTIVE
echo ========================================
echo.
echo Chunking Service: http://localhost:5009
echo Flask Main:       http://localhost:5008
echo.
echo Fichiers >200 lignes seront automatiquement
echo traites par le chunking service intelligent
echo.
echo Routes actives:
echo   /ai/organize  - Auto-detection + chunking
echo   /organize_large - Force chunking
echo.
pause
