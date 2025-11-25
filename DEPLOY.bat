@echo off
echo ========================================
echo   DEPLOIEMENT BACKEND GOOGLE APP ENGINE
echo ========================================
echo.

cd backend

echo [1/3] Installation dependances...
call npm install
if errorlevel 1 (
    echo ERREUR: Installation echouee
    pause
    exit /b 1
)

echo.
echo [2/3] Deploiement sur App Engine...
call gcloud app deploy --quiet
if errorlevel 1 (
    echo ERREUR: Deploiement echoue
    pause
    exit /b 1
)

echo.
echo [3/3] Recuperation URL...
for /f "tokens=*" %%i in ('gcloud app browse --no-launch-browser 2^>^&1 ^| findstr "https://"') do set URL=%%i

echo.
echo ========================================
echo   DEPLOIEMENT TERMINE !
echo ========================================
echo.
echo URL Backend: %URL%
echo.
echo Test: %URL%/api/health
echo.
pause
