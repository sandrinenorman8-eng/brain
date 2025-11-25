@echo off
REM Script simple pour ouvrir un dossier
REM Usage: open_folder_simple.bat "C:\path\to\folder"

set "FOLDER_PATH=%~1"

if "%FOLDER_PATH%"=="" (
    echo Erreur: Aucun chemin fourni
    exit /b 1
)

echo Ouverture du dossier: %FOLDER_PATH%

REM Méthode simple et directe
start "" "explorer.exe" "%FOLDER_PATH%"

echo Dossier ouvert !
exit /b 0
