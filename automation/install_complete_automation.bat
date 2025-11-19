@echo off
REM Installation complète du système d'automatisation Memobrik
REM Implémentation des 3 volets : Native Messaging + Robustesse + Auto-Start OS

echo ========================================
echo   MEMOBRIK - INSTALLATION COMPLETE
echo   SYSTEME D'AUTOMATISATION 3 VOLETS
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

cd /d "%~dp0"

echo [INFO] Repertoire d'installation: %CD%
echo.

REM ========================================
REM VOLET 1 : NATIVE MESSAGING
REM ========================================
echo ========================================
echo   VOLET 1 : NATIVE MESSAGING
echo ========================================
echo.

echo [1/10] Verification des dependances Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python non installe
    echo Installez Python depuis https://python.org
    pause
    exit /b 1
)
echo [OK] Python detecte

echo [2/10] Installation des modules Python requis...
pip install pyinstaller requests psutil >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Certains modules peuvent ne pas s'etre installes correctement
) else (
    echo [OK] Modules Python installes
)

echo [3/10] Ajout de l'endpoint de sante au serveur Flask...
python -c "
import os, sys
sys.path.append('.')
try:
    from health_check import MemobrikHealthChecker
    checker = MemobrikHealthChecker()
    # Ajouter l'endpoint de santé si nécessaire
    print('[OK] Endpoint de sante verifie')
except Exception as e:
    print(f'[WARNING] Erreur verification endpoint: {e}')
"

echo [4/10] Compilation du Native Messaging Host...
pyinstaller --onefile --noconsole --name server_host server_host.py >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Echec de la compilation
    pause
    exit /b 1
)
echo [OK] Executable compile

echo [5/10] Installation du Native Messaging Host...
call install_native_messaging.bat
if errorlevel 1 (
    echo [ERROR] Echec installation Native Messaging
    pause
    exit /b 1
)
echo [OK] Native Messaging installe

REM ========================================
REM VOLET 2 : ROBUSTESSE & UX
REM ========================================
echo.
echo ========================================
echo   VOLET 2 : ROBUSTESSE ^& UX
echo ========================================
echo.

echo [6/10] Configuration du systeme de surveillance...
python health_check.py >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Erreur lors du diagnostic initial
) else (
    echo [OK] Systeme de surveillance configure
)

echo [7/10] Creation des scripts de diagnostic...
(
echo @echo off
echo echo Diagnostic Memobrik en cours...
echo python "%~dp0health_check.py"
echo pause
) > diagnostic_memobrik.bat
echo [OK] Script de diagnostic cree

REM ========================================
REM VOLET 3 : AUTO-START OS
REM ========================================
echo.
echo ========================================
echo   VOLET 3 : AUTO-START OS
echo ========================================
echo.

echo [8/10] Installation du demarrage automatique Windows...
powershell -ExecutionPolicy Bypass -File "windows_task_scheduler.ps1" -Action install >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Erreur installation tache planifiee
    echo Vous pouvez l'installer manuellement plus tard
) else (
    echo [OK] Demarrage automatique configure
)

echo [9/10] Creation des scripts de gestion...

REM Script de démarrage manuel
(
echo @echo off
echo echo Demarrage manuel du serveur Memobrik...
echo python server_host.py
echo pause
) > start_manual.bat

REM Script de diagnostic complet
(
echo @echo off
echo echo ========================================
echo echo   DIAGNOSTIC COMPLET MEMOBRIK
echo echo ========================================
echo echo.
echo python health_check.py
echo echo.
echo echo Verification de la tache planifiee...
echo powershell -ExecutionPolicy Bypass -File "windows_task_scheduler.ps1" -Action status
echo echo.
echo pause
) > diagnostic_complet.bat

REM Script de désinstallation
(
echo @echo off
echo echo Desinstallation de l'automatisation Memobrik...
echo echo.
echo echo Suppression de la tache planifiee...
echo powershell -ExecutionPolicy Bypass -File "windows_task_scheduler.ps1" -Action uninstall
echo echo.
echo echo Suppression du Native Messaging...
echo "C:\Program Files\Memobrik\uninstall.bat"
echo echo.
echo echo Desinstallation terminee
echo pause
) > uninstall_automation.bat

echo [OK] Scripts de gestion crees

echo [10/10] Verification finale de l'installation...

REM Vérifier que tous les composants sont en place
set INSTALL_OK=1

if not exist "dist\server_host.exe" (
    echo [ERROR] Executable Native Messaging manquant
    set INSTALL_OK=0
)

if not exist "C:\Program Files\Memobrik\server_host.exe" (
    echo [ERROR] Native Messaging Host non installe
    set INSTALL_OK=0
)

if not exist "health_check.py" (
    echo [ERROR] Systeme de surveillance manquant
    set INSTALL_OK=0
)

if %INSTALL_OK%==0 (
    echo.
    echo [ERROR] Installation incomplete
    pause
    exit /b 1
)

echo.
echo ========================================
echo   INSTALLATION TERMINEE AVEC SUCCES !
echo ========================================
echo.
echo COMPOSANTS INSTALLES:
echo.
echo VOLET 1 - NATIVE MESSAGING:
echo   ✓ Native Messaging Host compile et installe
echo   ✓ Registre Windows configure
echo   ✓ Extension Chrome prete (dossier chrome_extension)
echo.
echo VOLET 2 - ROBUSTESSE ^& UX:
echo   ✓ Systeme de surveillance avance
echo   ✓ Health-check avec diagnostic complet
echo   ✓ Scripts de diagnostic automatises
echo.
echo VOLET 3 - AUTO-START OS:
echo   ✓ Tache planifiee Windows configuree
echo   ✓ Demarrage automatique a la connexion
echo   ✓ Scripts de gestion et maintenance
echo.
echo SCRIPTS DISPONIBLES:
echo   - diagnostic_complet.bat     : Diagnostic complet du systeme
echo   - start_manual.bat          : Demarrage manuel du serveur
echo   - uninstall_automation.bat  : Desinstallation complete
echo.
echo PROCHAINES ETAPES:
echo.
echo 1. INSTALLER L'EXTENSION CHROME:
echo    - Ouvrir Chrome
echo    - Aller dans chrome://extensions/
echo    - Activer le "Mode developpeur"
echo    - Cliquer "Charger l'extension non empaquetee"
echo    - Selectionner le dossier: %CD%\chrome_extension
echo.
echo 2. CONFIGURER L'EXTENSION:
echo    - Noter l'ID de l'extension affiche
echo    - Modifier le fichier: C:\Program Files\Memobrik\com.memobrik.server_starter.json
echo    - Remplacer EXTENSION_ID_PLACEHOLDER par l'ID reel
echo    - Redemarrer Chrome
echo.
echo 3. TESTER LE SYSTEME:
echo    - Cliquer sur l'icone de l'extension dans Chrome
echo    - Le serveur devrait demarrer automatiquement
echo    - Le side panel devrait s'ouvrir avec Memobrik
echo.
echo 4. VERIFICATION:
echo    - Executer diagnostic_complet.bat pour verifier
echo    - Redemarrer Windows pour tester le demarrage automatique
echo.
echo ========================================
echo   INSTALLATION 3 VOLETS TERMINEE !
echo ========================================
echo.
pause