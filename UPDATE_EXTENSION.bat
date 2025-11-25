@echo off
echo ========================================
echo   MISE A JOUR EXTENSION AVEC URL GAE
echo ========================================
echo.

echo [1/2] Recuperation URL backend...
for /f "tokens=*" %%i in ('gcloud app browse --no-launch-browser 2^>^&1 ^| findstr "https://"') do set BACKEND_URL=%%i

if "%BACKEND_URL%"=="" (
    echo ERREUR: Impossible de recuperer l'URL backend
    echo Verifie que le backend est deploye avec: DEPLOY.bat
    pause
    exit /b 1
)

echo URL Backend: %BACKEND_URL%
echo.

echo [2/2] Mise a jour manifest.json...
cd G:\memobrik\extchrome

powershell -Command "(Get-Content manifest.json) -replace 'http://localhost:5008', '%BACKEND_URL%' | Set-Content manifest.json"

echo.
echo ========================================
echo   MISE A JOUR TERMINEE !
echo ========================================
echo.
echo Extension: G:\memobrik\extchrome
echo Backend: %BACKEND_URL%
echo.
echo Prochaines etapes:
echo 1. Chrome ^> chrome://extensions/
echo 2. Recharger l'extension
echo 3. Tester !
echo.
pause
