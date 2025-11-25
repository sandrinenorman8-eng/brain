@echo off
echo ========================================
echo   BACKUP COMPLET DE MEMOBRIK
echo ========================================
echo.

cd /d "%~dp0"

REM Créer le dossier zip s'il n'existe pas
if not exist "zip" mkdir zip

REM Obtenir la date et l'heure
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set date_str=%datetime:~0,4%-%datetime:~4,2%-%datetime:~6,2%_%datetime:~8,2%-%datetime:~10,2%-%datetime:~12,2%

REM Nom du fichier de backup
set backup_file=zip\backup_memobrik_complet_%date_str%.zip

echo [INFO] Creation du backup...
echo [INFO] Source: %cd%
echo [INFO] Destination: %backup_file%
echo [INFO] Le dossier zip/ sera exclu du backup
echo.

REM Vérifier si PowerShell est disponible
powershell -Command "Write-Host 'PowerShell OK'" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] PowerShell non disponible
    echo Utilisez le bouton de backup dans l'application
    pause
    exit /b 1
)

REM Créer le backup avec PowerShell (exclure le dossier zip)
echo [1/2] Compression en cours...
powershell -Command "$items = Get-ChildItem -Path '.' -Exclude 'zip' | Where-Object { $_.Name -ne 'zip' }; Compress-Archive -Path $items -DestinationPath '.\%backup_file%' -CompressionLevel Optimal -Force"

if errorlevel 1 (
    echo [ERROR] Echec de la creation du backup
    pause
    exit /b 1
)

REM Vérifier la taille
echo.
echo [2/2] Verification...
for %%A in ("%backup_file%") do set size=%%~zA
set /a size_mb=%size% / 1048576

echo.
echo ========================================
echo   BACKUP TERMINE
echo ========================================
echo.
echo Fichier: %backup_file%
echo Taille: %size_mb% MB
echo.
echo Le backup contient TOUT le dossier memobrik:
echo - deuxieme_cerveau/
echo - Tous les autres fichiers et dossiers
echo - SAUF le dossier zip/ (contient les backups)
echo.
echo Emplacement: %cd%\%backup_file%
echo.
pause
