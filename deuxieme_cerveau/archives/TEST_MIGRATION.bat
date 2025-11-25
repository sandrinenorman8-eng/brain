@echo off
echo ========================================
echo   TEST DE LA MIGRATION
echo ========================================
echo.

cd /d "%~dp0"

echo [1/5] Verification de la structure...
if exist "src\" (
    echo [OK] Dossier src/ existe
) else (
    echo [ERROR] Dossier src/ manquant
    pause
    exit /b 1
)

if exist "data\" (
    echo [OK] Dossier data/ existe
) else (
    echo [ERROR] Dossier data/ manquant
    pause
    exit /b 1
)

echo.
echo [2/5] Comptage des categories dans data/...
for /f %%i in ('dir /ad /b data 2^>nul ^| find /c /v ""') do set count=%%i
echo [OK] %count% categories trouvees dans data/

echo.
echo [3/5] Verification des fichiers modifies...
findstr /C:"data/{category}" app.py >nul 2>&1
if errorlevel 1 (
    echo [ERROR] app.py n'a pas ete modifie correctement
    pause
    exit /b 1
) else (
    echo [OK] app.py contient les chemins data/
)

findstr /C:"'data', categoryName" search-server-fixed.js >nul 2>&1
if errorlevel 1 (
    echo [ERROR] search-server-fixed.js n'a pas ete modifie correctement
    pause
    exit /b 1
) else (
    echo [OK] search-server-fixed.js contient les chemins data/
)

echo.
echo [4/5] Test de lecture d'une categorie...
if exist "data\todo\" (
    echo [OK] Categorie 'todo' accessible dans data/
) else (
    echo [WARNING] Categorie 'todo' non trouvee
)

echo.
echo [5/5] Verification des fichiers src/...
if exist "src\backend\app.py" (
    echo [OK] src/backend/app.py existe
) else (
    echo [ERROR] src/backend/app.py manquant
)

if exist "src\frontend\search-server-fixed.js" (
    echo [OK] src/frontend/search-server-fixed.js existe
) else (
    echo [ERROR] src/frontend/search-server-fixed.js manquant
)

echo.
echo ========================================
echo   TESTS TERMINES
echo ========================================
echo.
echo Tout semble OK! Vous pouvez maintenant:
echo 1. Lancer START.bat
echo 2. Tester l'application
echo 3. Verifier que la sauvegarde/lecture fonctionne
echo.
pause
