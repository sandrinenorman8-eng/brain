@echo off
echo ========================================
echo   RESTART FLASK - FORCE RELOAD
echo ========================================
echo.

REM Tuer tous les processus Python
echo [1/2] Arret tous processus Python...
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak >nul

REM Redémarrer Flask
echo [2/2] Redemarrage Flask...
cd /d "%~dp0deuxieme_cerveau"
start "Flask Main" cmd /k "python app_new.py"

timeout /t 3 /nobreak >nul

REM Redémarrer Chunking
echo [3/3] Redemarrage Chunking Service...
start "Chunking Service" cmd /k "python chunking_service.py"

echo.
echo ========================================
echo   SERVICES REDEMARRES
echo ========================================
echo.
echo Flask:    http://localhost:5008
echo Chunking: http://localhost:5009
echo.
pause
