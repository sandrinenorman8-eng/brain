@echo off
echo ========================================
echo   DEMARRAGE COMPLET - 3 SERVICES
echo ========================================
echo.
echo [1/3] Flask Main App (Port 5008)
echo [2/3] Node Search Server (Port 3008)
echo [3/3] Chunking Service (Port 5009)
echo.
echo ========================================

REM Service 1: Flask Main
start "Flask Main (5008)" cmd /k "cd /d %~dp0deuxieme_cerveau && gunicorn -w 4 --threads 2 -b 0.0.0.0:5008 app:app"
timeout /t 3 /nobreak >nul

REM Service 2: Node Search
start "Node Search (3008)" cmd /k "cd /d %~dp0 && node search-server.js"
timeout /t 2 /nobreak >nul

REM Service 3: Chunking Service
start "Chunking Service (5009)" cmd /k "cd /d %~dp0deuxieme_cerveau && gunicorn -c gunicorn_config.py chunking_service:app"
timeout /t 2 /nobreak >nul

echo.
echo [OK] Tous les services sont demarres
echo.
echo URLs:
echo   - Main App:     http://localhost:5008
echo   - Search:       http://localhost:3008
echo   - Chunking:     http://localhost:5009
echo.
pause
