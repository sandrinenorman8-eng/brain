@echo off
echo ========================================
echo   Arret Chunking Service (Port 5009)
echo ========================================
echo.

REM Tuer processus Gunicorn sur port 5009
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5009') do (
    echo [INFO] Arret processus %%a
    taskkill /F /PID %%a
)

echo.
echo [OK] Chunking Service arrete
pause
