@echo off
if "%1"=="" (
    echo Usage: UPDATE_EXTENSION_NGROK.bat [URL_NGROK]
    echo Exemple: UPDATE_EXTENSION_NGROK.bat https://abc123.ngrok-free.app
    pause
    exit /b 1
)

set NGROK_URL=%1

echo ========================================
echo   MISE A JOUR EXTENSION AVEC NGROK
echo ========================================
echo.
echo URL ngrok: %NGROK_URL%
echo.

REM Mettre a jour manifest.json
powershell -Command "(Get-Content G:\memobrik\extchrome\manifest.json) -replace 'http://localhost:5008', '%NGROK_URL%' -replace 'https://.*\.appspot\.com', '%NGROK_URL%' | Set-Content G:\memobrik\extchrome\manifest.json"

REM Mettre a jour sidepanel.html
powershell -Command "(Get-Content G:\memobrik\extchrome\sidepanel.html) -replace 'http://localhost:5008', '%NGROK_URL%' -replace 'https://.*\.appspot\.com', '%NGROK_URL%' | Set-Content G:\memobrik\extchrome\sidepanel.html"

REM Mettre a jour loader.js
powershell -Command "(Get-Content G:\memobrik\extchrome\loader.js) -replace 'http://localhost:5008', '%NGROK_URL%' -replace 'https://.*\.appspot\.com', '%NGROK_URL%' | Set-Content G:\memobrik\extchrome\loader.js"

REM Mettre a jour background.js
powershell -Command "(Get-Content G:\memobrik\extchrome\background.js) -replace 'http://localhost:5008', '%NGROK_URL%' -replace 'https://.*\.appspot\.com', '%NGROK_URL%' | Set-Content G:\memobrik\extchrome\background.js"

echo.
echo ========================================
echo   EXTENSION MISE A JOUR !
echo ========================================
echo.
echo Extension: G:\memobrik\extchrome
echo URL: %NGROK_URL%
echo.
echo PROCHAINE ETAPE:
echo 1. Chrome ^> chrome://extensions/
echo 2. Recharger "Deuxieme Cerveau"
echo 3. Tester !
echo.
pause
