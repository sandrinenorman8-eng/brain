@echo off
echo ========================================
echo   Deuxieme Cerveau - Demarrage
echo ========================================
echo.

REM Verifier si Python est installe
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou n'est pas dans le PATH
    pause
    exit /b 1
)

REM Verifier si Node.js est installe
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Node.js n'est pas installe ou n'est pas dans le PATH
    pause
    exit /b 1
)

REM Verifier si les dependances Python sont installees
echo [INFO] Verification des dependances Python...
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installation des dependances Python...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERREUR] Echec de l'installation des dependances
        pause
        exit /b 1
    )
)

REM Demarrer le serveur de recherche Node.js
echo [INFO] Demarrage du serveur de recherche Node.js (port 3008)...
start "Search Server" cmd /k "node search-server-fixed.js"
timeout /t 2 /nobreak >nul

REM Demarrer le serveur Flask
echo [INFO] Demarrage du serveur Flask (port 5008)...
start "Flask Server" cmd /k "python app_new.py"
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo   Serveurs demarres avec succes!
echo ========================================
echo.
echo   Flask:  http://localhost:5008
echo   Search: http://localhost:3008
echo.
echo   Interface: http://localhost:5008
echo   Notes:     http://localhost:5008/all_notes
echo.
echo   Appuyez sur une touche pour ouvrir l'interface...
pause >nul

REM Ouvrir l'interface dans le navigateur
start http://localhost:5008

echo.
echo   Pour arreter les serveurs, utilisez STOP.bat
echo.
