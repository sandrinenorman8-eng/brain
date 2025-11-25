@echo off
cls
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║         TEST COMPLET CHUNKING SERVICE                      ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM 1. Vérifier que les services tournent
echo [1/3] Verification services...
netstat -an | findstr ":5008" >nul
if errorlevel 1 (
    echo [ERROR] Flask non detecte sur port 5008
    echo [ACTION] Lancer dans un autre terminal: cd deuxieme_cerveau ^&^& python app_new.py
    pause
    exit /b 1
)

netstat -an | findstr ":5009" >nul
if errorlevel 1 (
    echo [ERROR] Chunking service non detecte sur port 5009
    echo [ACTION] Lancer dans un autre terminal: cd deuxieme_cerveau ^&^& python chunking_service.py
    pause
    exit /b 1
)

echo [OK] Flask et Chunking services detectes
echo.

REM 2. Lancer test
echo [2/3] Lancement test automatique...
echo.
echo ========================================
echo   SURVEILLE LE TERMINAL CHUNKING
echo ========================================
echo.
echo Tu devrais voir:
echo   [DEBUG] /organize_large appele
echo   [DEBUG] Data recue: ...
echo   [DEBUG] Content: XXXXX chars
echo   [DEBUG] Debut chunking methode: smart
echo   [DEBUG] Chunking termine: XX chunks crees
echo   [DEBUG] Debut traitement AI de XX chunks
echo   [DEBUG] Traitement chunk 1/XX
echo   ...
echo.
pause

python TEST_FUSION_IA_AUTO.py

pause
