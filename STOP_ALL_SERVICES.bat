@echo off
echo ========================================
echo   ARRET COMPLET - 3 SERVICES
echo ========================================
echo.

REM Port 5008 - Flask Main
echo [1/3] Arret Flask Main (5008)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5008') do taskkill /F /PID %%a 2>nul

REM Port 3008 - Node Search
echo [2/3] Arret Node Search (3008)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :3008') do taskkill /F /PID %%a 2>nul

REM Port 5009 - Chunking Service
echo [3/3] Arret Chunking Service (5009)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5009') do taskkill /F /PID %%a 2>nul

echo.
echo [OK] Tous les services sont arretes
pause
