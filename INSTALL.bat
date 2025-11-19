@echo off
echo ========================================
echo   Deuxieme Cerveau - Installation
echo ========================================
echo.

REM Verifier si Python est installe
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou n'est pas dans le PATH
    echo.
    echo Telechargez Python depuis: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [INFO] Python detecte:
python --version
echo.

REM Verifier si pip est installe
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] pip n'est pas installe
    pause
    exit /b 1
)

echo [INFO] pip detecte:
pip --version
echo.

REM Installer les dependances Python
echo [INFO] Installation des dependances Python...
echo.
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [ERREUR] Echec de l'installation des dependances
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Installation terminee avec succes!
echo ========================================
echo.
echo Dependances installees:
echo   - Flask 3.0.0
echo   - python-dotenv 1.0.0
echo   - requests 2.32.3
echo   - flask-cors 4.0.0
echo   - pytest 7.4.3
echo   - pytest-flask 1.3.0
echo.
echo Vous pouvez maintenant demarrer l'application avec START_NEW.bat
echo.
pause
