@echo off
echo ========================================
echo   DEMARRAGE COMPLET SYSTEME
echo ========================================
echo.

REM Verifier si ngrok est installe
where ngrok >nul 2>&1
if %errorlevel% neq 0 (
    echo [ETAPE 1] Installation ngrok...
    echo.
    echo Telechargement ngrok...
    powershell -Command "Invoke-WebRequest -Uri 'https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip' -OutFile 'ngrok.zip'"
    powershell -Command "Expand-Archive -Path 'ngrok.zip' -DestinationPath '.' -Force"
    del ngrok.zip
    echo ngrok installe !
    echo.
)

echo [ETAPE 2] Demarrage Flask...
cd deuxieme_cerveau
start "Flask Backend" cmd /k "START.bat"
timeout /t 5 /nobreak >nul

echo [ETAPE 3] Demarrage ngrok tunnel...
cd ..
start "ngrok Tunnel" cmd /k "ngrok http 5008"

echo.
echo ========================================
echo   SYSTEME DEMARRE !
echo ========================================
echo.
echo 1. Flask: http://localhost:5008
echo 2. ngrok: Copie l'URL https dans la fenetre ngrok
echo 3. Backend GAE: https://top-operand-473602-h0.uc.r.appspot.com
echo.
echo PROCHAINE ETAPE:
echo - Copie l'URL ngrok (https://xxx.ngrok-free.app)
echo - Lance: UPDATE_FLASK_URL.bat [URL_NGROK]
echo.
pause
