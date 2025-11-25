@echo off
echo ========================================
echo   Deuxieme Cerveau - Tests
echo ========================================
echo.

REM Verifier si pytest est installe
python -c "import pytest" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installation de pytest...
    pip install pytest pytest-flask
)

echo [INFO] Execution des tests...
echo.

REM Executer les tests
pytest tests/ -v --tb=short

if errorlevel 1 (
    echo.
    echo [ERREUR] Certains tests ont echoue
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Tous les tests ont reussi!
echo ========================================
echo.
pause
