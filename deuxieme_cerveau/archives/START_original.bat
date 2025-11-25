@echo off
echo ========================================
echo   DEUXIEME CERVEAU - DEMARRAGE
echo ========================================
echo.

cd /d "%~dp0"
echo [DEBUG] Current directory: %cd%

REM Verification Python
echo [DEBUG] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python non installe
    pause
    exit /b 1
} else {
    echo [OK] Python is installed
}

REM Verification Node.js
echo [DEBUG] Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js non installe
    pause
    exit /b 1
) else {
    echo [OK] Node.js is installed
}

REM Check if required files exist in src directories
echo.
echo [DEBUG] Checking source files...

if exist "src\backend\app.py" (
    echo [OK] src\backend\app.py exists
) else {
    echo [ERROR] src\backend\app.py not found
    pause
    exit /b 1
}

if exist "src\frontend\index.html" (
    echo [OK] src\frontend\index.html exists
) else {
    echo [ERROR] src\frontend\index.html not found
    pause
    exit /b 1
}

if exist "src\frontend\search-server-fixed.js" (
    echo [OK] src\frontend\search-server-fixed.js exists
) else {
    echo [ERROR] src\frontend\search-server-fixed.js not found
    pause
    exit /b 1
}

REM Copier les fichiers depuis src
echo.
echo [1/6] Copie des fichiers depuis src...
if exist "src\backend\app.py" (
    copy /Y "src\backend\*.py" . >nul 2>&1
    copy /Y "src\backend\*.json" . >nul 2>&1
    echo [OK] Backend copie - Files copied: %ERRORLEVEL%
) else {
    echo [ERROR] src\backend non trouve
    pause
    exit /b 1
}

if exist "src\frontend\index.html" (
    copy /Y "src\frontend\*.html" . >nul 2>&1
    copy /Y "src\frontend\*.js" . >nul 2>&1
    echo [OK] Frontend copie - Files copied: %ERRORLEVEL%
) else {
    echo [ERROR] src\frontend non trouve
    pause
    exit /b 1
}

REM Verify copied files exist
echo.
echo [DEBUG] Verifying copied files...
if exist "app.py" (
    echo [OK] app.py copied successfully
) else {
    echo [ERROR] app.py not copied
}

if exist "index.html" (
    echo [OK] index.html copied successfully
) else {
    echo [ERROR] index.html not copied
}

if exist "search-server-fixed.js" (
    echo [OK] search-server-fixed.js copied successfully
) else {
    echo [ERROR] search-server-fixed.js not copied
}

REM Check if categories.json exists
if exist "categories.json" (
    echo [OK] categories.json exists
) else {
    echo [ERROR] categories.json not found
    pause
    exit /b 1
}

REM Check Python dependencies
echo.
echo [DEBUG] Checking Python dependencies...
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Flask not installed. Run: pip install flask
    pause
    exit /b 1
) else {
    echo [OK] Flask is installed
}

REM Tuer les anciens processus sur les ports
echo.
echo [2/6] Nettoyage des anciens processus...
echo [DEBUG] Checking processes on ports 5008 and 3008...
netstat -ano | findstr :5008 >nul 2>&1
if not errorlevel 1 (
    echo [INFO] Found processes on port 5008
    for /f "tokens=5" %%a in ('netstat -aon ^| find ":5008" ^| find "LISTENING"') do taskkill /F /PID %%a >nul 2>&1
    if not errorlevel 1 (
        echo [OK] Killed processes on port 5008
    ) else {
        echo [WARNING] Could not kill processes on port 5008
    }
) else {
    echo [OK] No processes on port 5008
}

netstat -ano | findstr :3008 >nul 2>&1
if not errorlevel 1 (
    echo [INFO] Found processes on port 3008
    for /f "tokens=5" %%a in ('netstat -aon ^| find ":3008" ^| find "LISTENING"') do taskkill /F /PID %%a >nul 2>&1
    if not errorlevel 1 (
        echo [OK] Killed processes on port 3008
    ) else {
        echo [WARNING] Could not kill processes on port 3008
    }
) else {
    echo [OK] No processes on port 3008
}

REM Demarrer le serveur de recherche Node.js
echo.
echo [3/6] Demarrage du serveur de recherche (port 3008)...
echo [DEBUG] Starting Node.js search server...
start "Search Server - Port 3008" cmd /c "node search-server-fixed.js"
timeout /t 3 /nobreak >nul
echo [OK] Search server demarre

REM Test if search server is running
echo.
echo [DEBUG] Testing search server connectivity...
timeout /t 2 /nobreak >nul
curl -s http://localhost:3008/status >nul 2>&1
if not errorlevel 1 (
    echo [OK] Search server is responding
) else {
    echo [WARNING] Search server not responding yet, continuing...
}

REM Ouvrir le navigateur apres 4 secondes
echo.
echo [4/6] Preparation du navigateur...
echo [DEBUG] Browser will open in 4 seconds...
start "" cmd /c "timeout /t 4 /nobreak >nul & start http://localhost:5008"

REM Demarrer Flask (bloquant)
echo.
echo [5/6] Demarrage du serveur Flask (port 5008)...
echo [DEBUG] Starting Flask server...
echo.
echo ========================================
echo   SERVEURS ACTIFS:
echo   - Flask:  http://localhost:5008
echo   - Search: http://localhost:3008
echo.
echo   Appuyez sur Ctrl+C pour arreter
echo ========================================
echo.

python app.py

echo.
echo [STOP] Serveur Flask arrete
echo.
echo ATTENTION: Le serveur de recherche tourne toujours
echo Fermez la fenetre "Search Server - Port 3008" manuellement
echo.
pause
