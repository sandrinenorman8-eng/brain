@echo off
echo ========================================
echo   ARRET DE TOUS LES SERVEURS
echo ========================================
echo.

REM Tuer les processus sur port 5008 (Flask)
echo [1/2] Arret du serveur Flask (port 5008)...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":5008" ^| find "LISTENING"') do (
    echo Arret du processus PID %%a
    taskkill /F /PID %%a
)

REM Tuer les processus sur port 3008 (Search)
echo.
echo [2/2] Arret du serveur de recherche (port 3008)...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":3008" ^| find "LISTENING"') do (
    echo Arret du processus PID %%a
    taskkill /F /PID %%a
)

echo.
echo [OK] Tous les serveurs sont arretes
echo.
pause
