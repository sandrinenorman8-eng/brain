@echo off
echo ========================================
echo   DEMARRAGE DEUXIEME CERVEAU
echo ========================================
echo.

REM Demarrer Flask
echo [1/2] Demarrage du serveur Flask...
start "Flask Server" cmd /k "python app_new.py"
timeout /t 3 /nobreak >nul

REM Demarrer Node.js
echo [2/2] Demarrage du serveur de recherche...
start "Search Server" cmd /k "node search-server-fixed.js"
timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo   SERVEURS DEMARRES !
echo ========================================
echo.
echo   Flask:      http://localhost:5008
echo   Recherche:  http://localhost:3008
echo   Fusion IA:  http://localhost:5008/fusion_intelligente
echo.
echo   Appuyez sur une touche pour ouvrir dans le navigateur...
pause >nul

start http://localhost:5008

echo.
echo Pour arreter les serveurs, fermez les fenetres CMD
echo.
