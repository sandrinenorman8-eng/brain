@echo off
echo ========================================
echo   DEUXIEME CERVEAU - DEMARRAGE
echo ========================================
echo.

cd /d "%~dp0"

REM Verification Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python non installe
    pause
    exit /b 1
)

REM Verification Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js non installe
    pause
    exit /b 1
)

REM Vérifier que les fichiers existent
echo [1/5] Verification des fichiers...
if not exist "app_new.py" (
    echo [ERROR] app_new.py non trouve
    pause
    exit /b 1
)
if not exist "index.html" (
    echo [ERROR] index.html non trouve
    pause
    exit /b 1
)
if not exist "category_path_resolver.py" (
    echo [ERROR] category_path_resolver.py non trouve
    pause
    exit /b 1
)
echo [OK] Tous les fichiers sont presents

REM Tuer les anciens processus sur les ports
echo.
echo [2/4] Nettoyage des anciens processus...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":5008" ^| find "LISTENING"') do taskkill /F /PID %%a >nul 2>&1
echo [OK] Ports liberes

REM Ouvrir le navigateur apres 3 secondes
echo.
echo [3/4] Preparation du navigateur...
start "" cmd /c "timeout /t 3 /nobreak >nul & start http://localhost:5008"

REM Demarrer Flask (bloquant)
echo.
echo [4/4] Demarrage du serveur Flask (port 5008)...
echo.
echo ========================================
echo   SERVEUR ACTIF:
echo   - Flask avec recherche integree: http://localhost:5008
echo.
echo   Appuyez sur Ctrl+C pour arreter
echo ========================================
echo.

python app_new.py

echo.
echo [STOP] Serveur Flask arrete
echo.
pause
