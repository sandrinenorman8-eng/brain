@echo off
title Deuxieme Cerveau v2.0 - Demarrage Rapide
color 0A

echo.
echo ================================================================================
echo                    DEUXIEME CERVEAU v2.0 - DEMARRAGE RAPIDE
echo ================================================================================
echo.
echo Ce script va:
echo   1. Verifier l'installation
echo   2. Installer les dependances si necessaire
echo   3. Executer les tests
echo   4. Demarrer l'application
echo.
echo Appuyez sur une touche pour continuer ou CTRL+C pour annuler...
pause >nul

echo.
echo ================================================================================
echo   ETAPE 1/4: VERIFICATION DE L'INSTALLATION
echo ================================================================================
echo.

REM Verifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe!
    echo.
    echo Telechargez Python depuis: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)
echo [OK] Python installe

REM Verifier Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Node.js n'est pas installe!
    echo.
    echo Telechargez Node.js depuis: https://nodejs.org/
    echo.
    pause
    exit /b 1
)
echo [OK] Node.js installe

echo.
echo ================================================================================
echo   ETAPE 2/4: INSTALLATION DES DEPENDANCES
echo ================================================================================
echo.

REM Verifier si Flask est installe
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installation des dependances Python...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERREUR] Echec de l'installation
        pause
        exit /b 1
    )
    echo [OK] Dependances installees
) else (
    echo [OK] Dependances deja installees
)

echo.
echo ================================================================================
echo   ETAPE 3/4: EXECUTION DES TESTS
echo ================================================================================
echo.

REM Verifier si pytest est installe
python -c "import pytest" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installation de pytest...
    pip install pytest pytest-flask
)

echo [INFO] Execution des tests...
pytest tests/ -v --tb=short
if errorlevel 1 (
    echo.
    echo [AVERTISSEMENT] Certains tests ont echoue
    echo Voulez-vous continuer quand meme? (O/N)
    set /p CONTINUE=
    if /i not "%CONTINUE%"=="O" (
        echo Demarrage annule
        pause
        exit /b 1
    )
) else (
    echo [OK] Tous les tests ont reussi!
)

echo.
echo ================================================================================
echo   ETAPE 4/4: DEMARRAGE DE L'APPLICATION
echo ================================================================================
echo.

echo [INFO] Demarrage du serveur de recherche Node.js...
start "Search Server" cmd /k "node search-server-fixed.js"
timeout /t 2 /nobreak >nul

echo [INFO] Demarrage du serveur Flask...
start "Flask Server" cmd /k "python app_new.py"
timeout /t 3 /nobreak >nul

echo.
echo ================================================================================
echo                    DEMARRAGE REUSSI!
echo ================================================================================
echo.
echo   Serveurs demarres:
echo     - Flask:  http://localhost:5008
echo     - Search: http://localhost:3008
echo.
echo   Acces:
echo     - Interface: http://localhost:5008
echo     - Notes:     http://localhost:5008/all_notes
echo.
echo   Pour arreter: STOP_NEW.bat
echo.
echo   Ouverture du navigateur dans 3 secondes...
timeout /t 3 /nobreak >nul

start http://localhost:5008

echo.
echo   Application demarree avec succes!
echo   Consultez les fenetres ouvertes pour voir les logs.
echo.
echo   Documentation:
echo     - Guide rapide:  QUICK_START.md
echo     - Documentation: README.md
echo     - API:           API.md
echo.
pause
