@echo off
echo ========================================
echo   SERVEUR DE RECHERCHE STANDALONE
echo ========================================
echo.
echo Ce script demarre uniquement le serveur de recherche
echo Pour demarrer l'application complete, utilisez START.bat
echo.

REM Verification Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js non installe
    echo Installez Node.js depuis https://nodejs.org/
    pause
    exit /b 1
)

REM Copier le serveur depuis src si necessaire
if exist "src\frontend\search-server.js" (
    copy /Y "src\frontend\search-server.js" . >nul 2>&1
    echo [OK] Serveur copie depuis src
)

REM Verifier que le fichier existe
if not exist "search-server.js" (
    echo [ERROR] search-server.js non trouve
    pause
    exit /b 1
)

echo.
echo [START] Demarrage du serveur de recherche (port 3008)...
echo.
echo ========================================
echo   SERVEUR ACTIF: http://localhost:3008
echo   Appuyez sur Ctrl+C pour arreter
echo ========================================
echo.

node search-server-fixed.js

echo.
echo [STOP] Serveur arrete
pause




