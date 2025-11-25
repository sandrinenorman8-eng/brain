@echo off
echo ========================================
echo   Deuxieme Cerveau - Arret
echo ========================================
echo.

echo [INFO] Arret du serveur Flask...
taskkill /FI "WINDOWTITLE eq Flask Server*" /T /F >nul 2>&1

echo [INFO] Arret du serveur de recherche Node.js...
taskkill /FI "WINDOWTITLE eq Search Server*" /T /F >nul 2>&1

REM Alternative: tuer tous les processus Python et Node
REM taskkill /IM python.exe /F >nul 2>&1
REM taskkill /IM node.exe /F >nul 2>&1

echo.
echo ========================================
echo   Serveurs arretes avec succes!
echo ========================================
echo.
pause
