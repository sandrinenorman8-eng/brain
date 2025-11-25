@echo off
echo ========================================
echo   INSTALLATION GOOGLE CLOUD SDK
echo ========================================
echo.
echo Telechargement en cours...
echo.

powershell -Command "Start-Process 'https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe'"

echo.
echo ========================================
echo   INSTRUCTIONS
echo ========================================
echo.
echo 1. L'installateur va s'ouvrir
echo 2. Suivre les etapes d'installation
echo 3. Cocher "Run gcloud init"
echo 4. Se connecter avec ton compte Google
echo 5. Selectionner ton projet
echo.
echo Apres installation, relancer: DEPLOY_TOUT.bat
echo.
pause
