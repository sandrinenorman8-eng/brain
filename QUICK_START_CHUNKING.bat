@echo off
cls
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║         CHUNKING SERVICE - DEMARRAGE RAPIDE                ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo [INFO] Demarrage Chunking Service sur port 5009...
echo.

cd /d "%~dp0deuxieme_cerveau"
python chunking_service.py

pause
