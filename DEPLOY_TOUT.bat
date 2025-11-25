@echo off
echo ========================================
echo   DEPLOIEMENT COMPLET
echo   Backend + Extension
echo ========================================
echo.

echo ETAPE 1/2: Deploiement Backend GAE
echo ========================================
call DEPLOY.bat
if errorlevel 1 (
    echo ERREUR lors du deploiement backend
    pause
    exit /b 1
)

echo.
echo.
echo ETAPE 2/2: Mise a jour Extension
echo ========================================
call UPDATE_EXTENSION.bat

echo.
echo ========================================
echo   DEPLOIEMENT COMPLET TERMINE !
echo ========================================
echo.
echo Extension prete dans: G:\memobrik\extchrome
echo.
echo Prochaines etapes:
echo 1. Chrome ^> chrome://extensions/
echo 2. Recharger l'extension "Deuxieme Cerveau"
echo 3. Cliquer sur l'icone pour ouvrir le side panel
echo.
pause
