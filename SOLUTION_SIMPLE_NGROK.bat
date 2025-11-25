@echo off
echo ========================================
echo   SOLUTION SIMPLE - NGROK SEULEMENT
echo ========================================
echo.

REM Verifier si ngrok est installe
where ngrok >nul 2>&1
if %errorlevel% neq 0 (
    echo [1/3] Installation ngrok...
    echo.
    powershell -Command "Invoke-WebRequest -Uri 'https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip' -OutFile 'ngrok.zip'"
    powershell -Command "Expand-Archive -Path 'ngrok.zip' -DestinationPath '.' -Force"
    del ngrok.zip
    echo ngrok installe !
    echo.
)

echo [2/3] Demarrage Flask...
cd deuxieme_cerveau
start "Flask Backend" cmd /k "START.bat"
timeout /t 5 /nobreak >nul
cd ..

echo [3/3] Demarrage ngrok...
start "ngrok Tunnel" cmd /k "ngrok http 5008"

timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo   SYSTEME DEMARRE !
echo ========================================
echo.
echo 1. Flask local: http://localhost:5008
echo 2. ngrok public: Regarde la fenetre ngrok
echo.
echo PROCHAINE ETAPE:
echo 1. Copie l'URL ngrok (https://xxx.ngrok-free.app)
echo 2. Mets-la dans l'extension:
echo    - Ouvre G:\memobrik\extchrome\manifest.json
echo    - Remplace localhost:5008 par l'URL ngrok
echo    - Recharge l'extension dans Chrome
echo.
echo C'EST TOUT ! Pas besoin de GAE !
echo.
pause
