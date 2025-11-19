@echo off
REM Volet 1 Phase B : Installation Native Messaging + Registre Windows
echo ========================================
echo   INSTALLATION NATIVE MESSAGING
echo ========================================
echo.

REM Vérifier les privilèges administrateur
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [OK] Privileges administrateur detectes
) else (
    echo [ERROR] Ce script necessite des privileges administrateur
    echo Clic droit sur le fichier et "Executer en tant qu'administrateur"
    pause
    exit /b 1
)

REM Créer le dossier d'installation
set INSTALL_DIR=C:\Program Files\Memobrik
echo [1/5] Creation du dossier d'installation...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
echo [OK] Dossier cree: %INSTALL_DIR%

REM Compiler le script Python en exécutable
echo.
echo [2/5] Compilation du Native Messaging Host...
cd /d "%~dp0"

REM Vérifier que PyInstaller est installé
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installation de PyInstaller...
    pip install pyinstaller requests
    if errorlevel 1 (
        echo [ERROR] Impossible d'installer PyInstaller
        pause
        exit /b 1
    )
)

REM Compiler l'exécutable
pyinstaller --onefile --noconsole --name server_host server_host.py
if errorlevel 1 (
    echo [ERROR] Echec de la compilation
    pause
    exit /b 1
)

REM Copier l'exécutable
copy /Y "dist\server_host.exe" "%INSTALL_DIR%\server_host.exe"
if errorlevel 1 (
    echo [ERROR] Impossible de copier l'executable
    pause
    exit /b 1
)
echo [OK] Executable copie

REM Créer le manifest Native Messaging
echo.
echo [3/5] Creation du manifest Native Messaging...
set MANIFEST_FILE=%INSTALL_DIR%\com.memobrik.server_starter.json

(
echo {
echo   "name": "com.memobrik.server_starter",
echo   "description": "Memobrik Server Auto-Starter",
echo   "path": "C:\\Program Files\\Memobrik\\server_host.exe",
echo   "type": "stdio",
echo   "allowed_origins": [
echo     "chrome-extension://EXTENSION_ID_PLACEHOLDER/"
echo   ]
echo }
) > "%MANIFEST_FILE%"

echo [OK] Manifest cree: %MANIFEST_FILE%

REM Enregistrer dans le registre Windows
echo.
echo [4/5] Enregistrement dans le registre Windows...
reg add "HKCU\Software\Google\Chrome\NativeMessagingHosts\com.memobrik.server_starter" /ve /t REG_SZ /d "%MANIFEST_FILE%" /f >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Echec de l'enregistrement dans le registre
    pause
    exit /b 1
)
echo [OK] Registre mis a jour

REM Créer un script de désinstallation
echo.
echo [5/5] Creation du script de desinstallation...
set UNINSTALL_SCRIPT=%INSTALL_DIR%\uninstall.bat

(
echo @echo off
echo echo Desinstallation de Memobrik Native Messaging...
echo reg delete "HKCU\Software\Google\Chrome\NativeMessagingHosts\com.memobrik.server_starter" /f ^>nul 2^>^&1
echo rmdir /s /q "%INSTALL_DIR%"
echo echo Desinstallation terminee
echo pause
) > "%UNINSTALL_SCRIPT%"

echo [OK] Script de desinstallation cree

echo.
echo ========================================
echo   INSTALLATION TERMINEE !
echo ========================================
echo.
echo Fichiers installes:
echo - %INSTALL_DIR%\server_host.exe
echo - %MANIFEST_FILE%
echo - %UNINSTALL_SCRIPT%
echo.
echo PROCHAINES ETAPES:
echo 1. Installer l'extension Chrome
echo 2. Remplacer EXTENSION_ID_PLACEHOLDER dans le manifest
echo 3. Redemarrer Chrome
echo.
echo Pour desinstaller: Executer %UNINSTALL_SCRIPT%
echo.
pause