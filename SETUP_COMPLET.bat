@echo off
setlocal enabledelayedexpansion

echo ========================================
echo   SETUP COMPLET GAE + EXTENSION
echo ========================================
echo.

REM Verifier si gcloud est installe
where gcloud >nul 2>&1
if %errorlevel% neq 0 (
    echo [ETAPE 1/5] Installation Google Cloud SDK
    echo ========================================
    echo.
    echo Google Cloud SDK n'est pas installe.
    echo L'installateur va s'ouvrir...
    echo.
    echo IMPORTANT: Apres installation:
    echo 1. Cocher "Run gcloud init"
    echo 2. Se connecter avec compte Google
    echo 3. Selectionner le projet
    echo 4. Relancer ce script
    echo.
    pause
    
    start https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe
    
    echo.
    echo Attente installation...
    echo Relance ce script apres installation.
    pause
    exit /b 0
)

echo [ETAPE 1/5] Google Cloud SDK - OK
echo ========================================
echo.

REM Verifier authentification
gcloud auth list --filter=status:ACTIVE --format="value(account)" >nul 2>&1
if %errorlevel% neq 0 (
    echo [ETAPE 2/5] Authentification Google Cloud
    echo ========================================
    echo.
    echo Connexion a Google Cloud...
    gcloud auth login
    if %errorlevel% neq 0 (
        echo ERREUR: Authentification echouee
        pause
        exit /b 1
    )
)

echo [ETAPE 2/5] Authentification - OK
echo ========================================
echo.

REM Verifier projet configure
for /f "delims=" %%i in ('gcloud config get-value project 2^>nul') do set PROJECT_ID=%%i
if "%PROJECT_ID%"=="" (
    echo [ETAPE 3/5] Configuration Projet
    echo ========================================
    echo.
    echo Aucun projet configure.
    echo Liste des projets disponibles:
    echo.
    gcloud projects list
    echo.
    set /p PROJECT_ID="Entre le PROJECT_ID: "
    gcloud config set project !PROJECT_ID!
)

echo [ETAPE 3/5] Projet: %PROJECT_ID% - OK
echo ========================================
echo.

REM Verifier App Engine existe
gcloud app describe >nul 2>&1
if %errorlevel% neq 0 (
    echo [ETAPE 4/5] Creation App Engine
    echo ========================================
    echo.
    echo App Engine n'existe pas encore.
    echo Creation en cours (region: europe-west1)...
    gcloud app create --region=europe-west1
    if %errorlevel% neq 0 (
        echo.
        echo ERREUR: Creation App Engine echouee
        echo Verifie que la facturation est activee:
        echo https://console.cloud.google.com/billing
        pause
        exit /b 1
    )
)

echo [ETAPE 4/5] App Engine - OK
echo ========================================
echo.

echo [ETAPE 5/5] Deploiement Backend
echo ========================================
echo.

cd backend
echo Installation dependances...
call npm install --silent
if %errorlevel% neq 0 (
    echo ERREUR: Installation dependances echouee
    pause
    exit /b 1
)

echo.
echo Deploiement sur App Engine...
call gcloud app deploy --quiet
if %errorlevel% neq 0 (
    echo ERREUR: Deploiement echoue
    pause
    exit /b 1
)

echo.
echo Recuperation URL...
for /f "tokens=*" %%i in ('gcloud app browse --no-launch-browser 2^>^&1 ^| findstr "https://"') do set BACKEND_URL=%%i

cd ..

echo.
echo ========================================
echo   BACKEND DEPLOYE !
echo ========================================
echo.
echo URL: %BACKEND_URL%
echo.

REM Mise a jour extension
echo Mise a jour extension...
cd G:\memobrik\extchrome
powershell -Command "(Get-Content manifest.json) -replace 'http://localhost:5008', '%BACKEND_URL%' | Set-Content manifest.json"

echo.
echo ========================================
echo   SETUP TERMINE !
echo ========================================
echo.
echo Backend: %BACKEND_URL%
echo Extension: G:\memobrik\extchrome
echo.
echo PROCHAINES ETAPES:
echo 1. Chrome ^> chrome://extensions/
echo 2. Recharger "Deuxieme Cerveau"
echo 3. Tester !
echo.
pause
