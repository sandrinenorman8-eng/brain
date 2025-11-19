@echo off
echo ========================================
echo   Verification de l'installation
echo ========================================
echo.

set ERROR_COUNT=0

REM Verifier Python
echo [1/10] Verification de Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python non installe
    set /a ERROR_COUNT+=1
) else (
    echo [OK] Python installe
)

REM Verifier Node.js
echo [2/10] Verification de Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Node.js non installe
    set /a ERROR_COUNT+=1
) else (
    echo [OK] Node.js installe
)

REM Verifier Flask
echo [3/10] Verification de Flask...
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Flask non installe
    set /a ERROR_COUNT+=1
) else (
    echo [OK] Flask installe
)

REM Verifier python-dotenv
echo [4/10] Verification de python-dotenv...
python -c "import dotenv" >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] python-dotenv non installe
    set /a ERROR_COUNT+=1
) else (
    echo [OK] python-dotenv installe
)

REM Verifier requests
echo [5/10] Verification de requests...
python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] requests non installe
    set /a ERROR_COUNT+=1
) else (
    echo [OK] requests installe
)

REM Verifier flask-cors
echo [6/10] Verification de flask-cors...
python -c "import flask_cors" >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] flask-cors non installe
    set /a ERROR_COUNT+=1
) else (
    echo [OK] flask-cors installe
)

REM Verifier pytest
echo [7/10] Verification de pytest...
python -c "import pytest" >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] pytest non installe
    set /a ERROR_COUNT+=1
) else (
    echo [OK] pytest installe
)

REM Verifier structure des dossiers
echo [8/10] Verification de la structure...
if not exist "config" (
    echo [ERREUR] Dossier config manquant
    set /a ERROR_COUNT+=1
) else if not exist "utils" (
    echo [ERREUR] Dossier utils manquant
    set /a ERROR_COUNT+=1
) else if not exist "services" (
    echo [ERREUR] Dossier services manquant
    set /a ERROR_COUNT+=1
) else if not exist "blueprints" (
    echo [ERREUR] Dossier blueprints manquant
    set /a ERROR_COUNT+=1
) else if not exist "tests" (
    echo [ERREUR] Dossier tests manquant
    set /a ERROR_COUNT+=1
) else (
    echo [OK] Structure des dossiers correcte
)

REM Verifier fichiers principaux
echo [9/10] Verification des fichiers...
if not exist "app_new.py" (
    echo [ERREUR] app_new.py manquant
    set /a ERROR_COUNT+=1
) else if not exist "requirements.txt" (
    echo [ERREUR] requirements.txt manquant
    set /a ERROR_COUNT+=1
) else if not exist "README.md" (
    echo [ERREUR] README.md manquant
    set /a ERROR_COUNT+=1
) else (
    echo [OK] Fichiers principaux presents
)

REM Verifier imports Python
echo [10/10] Verification des imports...
python -c "from config.config import Config; from utils.response_utils import success_response; from services.category_service import load_categories" >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Probleme d'imports Python
    set /a ERROR_COUNT+=1
) else (
    echo [OK] Imports Python fonctionnels
)

echo.
echo ========================================
if %ERROR_COUNT%==0 (
    echo   Installation COMPLETE et VALIDE!
    echo ========================================
    echo.
    echo Tout est pret! Vous pouvez:
    echo   1. Demarrer l'application: START_NEW.bat
    echo   2. Executer les tests: RUN_TESTS.bat
    echo   3. Lire la doc: README.md
    echo.
) else (
    echo   %ERROR_COUNT% erreur(s) detectee(s)
    echo ========================================
    echo.
    echo Veuillez corriger les erreurs ci-dessus.
    echo Pour installer les dependances: INSTALL.bat
    echo.
)

pause
