@echo off
REM Script de vérification de l'installation complète
echo ========================================
echo   VERIFICATION INSTALLATION MEMOBRIK
echo ========================================
echo.

cd /d "%~dp0"

set ERRORS=0

echo [1/8] Verification des fichiers d'automation...
if not exist "server_host.py" (
    echo [ERROR] server_host.py manquant
    set /a ERRORS+=1
) else (
    echo [OK] server_host.py present
)

if not exist "health_check.py" (
    echo [ERROR] health_check.py manquant
    set /a ERRORS+=1
) else (
    echo [OK] health_check.py present
)

if not exist "windows_task_scheduler.ps1" (
    echo [ERROR] windows_task_scheduler.ps1 manquant
    set /a ERRORS+=1
) else (
    echo [OK] windows_task_scheduler.ps1 present
)

echo.
echo [2/8] Verification de l'executable Native Messaging...
if not exist "C:\Program Files\Memobrik\server_host.exe" (
    echo [ERROR] Native Messaging Host non installe
    set /a ERRORS+=1
) else (
    echo [OK] Native Messaging Host installe
)

echo.
echo [3/8] Verification du manifest Native Messaging...
if not exist "C:\Program Files\Memobrik\com.memobrik.server_starter.json" (
    echo [ERROR] Manifest Native Messaging manquant
    set /a ERRORS+=1
) else (
    echo [OK] Manifest Native Messaging present
    
    REM Vérifier le contenu du manifest
    findstr "EXTENSION_ID_PLACEHOLDER" "C:\Program Files\Memobrik\com.memobrik.server_starter.json" >nul
    if not errorlevel 1 (
        echo [WARNING] ID d'extension non configure dans le manifest
        echo           Remplacez EXTENSION_ID_PLACEHOLDER par l'ID reel
    ) else (
        echo [OK] ID d'extension configure
    )
)

echo.
echo [4/8] Verification de l'extension Chrome...
if not exist "chrome_extension\manifest.json" (
    echo [ERROR] Extension Chrome manquante
    set /a ERRORS+=1
) else (
    echo [OK] Extension Chrome presente
)

if not exist "chrome_extension\background.js" (
    echo [ERROR] Background script manquant
    set /a ERRORS+=1
) else (
    echo [OK] Background script present
)

if not exist "chrome_extension\sidepanel.html" (
    echo [ERROR] Side panel manquant
    set /a ERRORS+=1
) else (
    echo [OK] Side panel present
)

echo.
echo [5/8] Verification des dependances Python...
python -c "import requests, psutil" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Dependances Python manquantes
    echo         Executez: pip install requests psutil
    set /a ERRORS+=1
) else (
    echo [OK] Dependances Python installees
)

echo.
echo [6/8] Verification du serveur Flask...
if not exist "..\app.py" (
    echo [ERROR] Serveur Flask manquant
    set /a ERRORS+=1
) else (
    echo [OK] Serveur Flask present
    
    REM Vérifier l'endpoint de santé
    findstr "/health" "..\app.py" >nul
    if errorlevel 1 (
        echo [WARNING] Endpoint de sante manquant dans app.py
    ) else (
        echo [OK] Endpoint de sante present
    )
)

echo.
echo [7/8] Verification de la tache planifiee...
powershell -ExecutionPolicy Bypass -Command "Get-ScheduledTask -TaskName 'MemobrikAutoStart' -ErrorAction SilentlyContinue" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Tache planifiee non installee
    echo           Executez: powershell windows_task_scheduler.ps1 -Action install
) else (
    echo [OK] Tache planifiee installee
)

echo.
echo [8/8] Test de connectivite serveur...
python -c "
import requests
try:
    r = requests.get('http://localhost:5008/health', timeout=3)
    if r.status_code == 200:
        print('[OK] Serveur repond correctement')
    else:
        print('[WARNING] Serveur repond avec code:', r.status_code)
except:
    print('[INFO] Serveur non demarre (normal si pas encore lance)')
" 2>nul

echo.
echo ========================================
echo   RESULTAT DE LA VERIFICATION
echo ========================================

if %ERRORS%==0 (
    echo.
    echo ✅ INSTALLATION COMPLETE ET FONCTIONNELLE !
    echo.
    echo Prochaines etapes:
    echo 1. Installer l'extension Chrome depuis chrome://extensions/
    echo 2. Configurer l'ID d'extension dans le manifest
    echo 3. Tester en cliquant sur l'icone de l'extension
    echo.
    echo Scripts utiles:
    echo - diagnostic_complet.bat     : Diagnostic approfondi
    echo - test_automation.py         : Tests automatises
    echo - start_manual.bat          : Demarrage manuel
    echo.
) else (
    echo.
    echo ❌ INSTALLATION INCOMPLETE
    echo.
    echo %ERRORS% erreur(s) detectee(s)
    echo Consultez les messages ci-dessus pour corriger les problemes
    echo.
    echo Pour reinstaller:
    echo 1. Executez uninstall_automation.bat
    echo 2. Executez install_complete_automation.bat
    echo.
)

echo ========================================
pause