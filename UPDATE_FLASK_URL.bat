@echo off
if "%1"=="" (
    echo Usage: UPDATE_FLASK_URL.bat [URL_NGROK]
    echo Exemple: UPDATE_FLASK_URL.bat https://abc123.ngrok-free.app
    pause
    exit /b 1
)

set NGROK_URL=%1

echo ========================================
echo   MISE A JOUR URL FLASK
echo ========================================
echo.
echo URL ngrok: %NGROK_URL%
echo.

cd backend

REM Mettre a jour app.yaml
powershell -Command "(Get-Content app.yaml) -replace 'FLASK_URL:.*', 'FLASK_URL: \"%NGROK_URL%\"' | Set-Content app.yaml"

echo Deploiement sur GAE...
gcloud app deploy --quiet

echo.
echo ========================================
echo   MISE A JOUR TERMINEE !
echo ========================================
echo.
echo Backend GAE pointe maintenant vers: %NGROK_URL%
echo Extension Chrome prete !
echo.
pause
