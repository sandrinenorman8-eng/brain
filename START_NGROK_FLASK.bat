@echo off
echo ========================================
echo   NGROK TUNNEL - Flask App (Port 5008)
echo ========================================
echo.

REM Vérifier si Flask tourne
netstat -an | findstr :5008 >nul
if errorlevel 1 (
    echo [WARN] Flask ne semble pas tourner sur port 5008
    echo [INFO] Lancer START_ALL_SERVICES.bat d'abord
    echo.
    pause
    exit /b 1
)

echo [OK] Flask detecte sur port 5008
echo.
echo [INFO] Demarrage ngrok...
echo.

REM Lancer ngrok
ngrok.exe http 5008

pause
