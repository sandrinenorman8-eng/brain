@echo off
REM Script pour ouvrir un dossier dans l'Explorateur Windows
REM Utilisation: open_folder.bat "chemin_du_dossier"

if "%~1"=="" (
    echo Erreur: Aucun chemin fourni
    exit /b 1
)

echo Ouverture du dossier: %~1

REM Essayer d'ouvrir avec explorer.exe
start "" explorer "%~1"

REM Attendre un peu pour que ça s'ouvre
timeout /t 1 /nobreak >nul

echo Script termine - Dossier devrait etre ouvert
exit /b 0
