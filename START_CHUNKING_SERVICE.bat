@echo off
echo ========================================
echo   Demarrage Chunking Service (Port 5009)
echo ========================================
echo.

cd /d "%~dp0deuxieme_cerveau"

REM Creer dossier logs si inexistant
if not exist "logs" mkdir logs

echo [INFO] Lancement Gunicorn avec 4 workers...
gunicorn -c gunicorn_config.py chunking_service:app

pause
