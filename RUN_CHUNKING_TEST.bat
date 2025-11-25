@echo off
echo ========================================
echo   TEST CHUNKING - Fichier Volumineux
echo ========================================
echo.
echo Fichier: fusion_globale_2025-11-20_10-14-43.txt
echo Taille: 11,115 lignes / 760,144 caracteres
echo.
echo ========================================
echo.

REM Vérifier services
echo [1/3] Verification services...
netstat -an | findstr :5008 >nul
if errorlevel 1 (
    echo [WARN] Flask Main non detecte sur port 5008
    echo [ACTION] Lancer: START_ALL_SERVICES.bat
    pause
    exit /b 1
)

netstat -an | findstr :5009 >nul
if errorlevel 1 (
    echo [WARN] Chunking Service non detecte sur port 5009
    echo [ACTION] Lancer: START_CHUNKING_SERVICE.bat
    pause
    exit /b 1
)

echo [OK] Services detectes
echo.

REM Installer dépendances si nécessaire
echo [2/3] Verification dependencies...
pip show tiktoken >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installation tiktoken...
    pip install tiktoken
)

echo [OK] Dependencies OK
echo.

REM Lancer test
echo [3/3] Lancement test...
echo.
python TEST_CHUNKING_LARGE_FILE.py

pause
