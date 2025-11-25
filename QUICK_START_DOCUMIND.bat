@echo off
echo ========================================
echo DOCUMIND RAG - Quick Start
echo ========================================
echo.

REM Check if Gemini API key is set
if not defined GEMINI_API_KEY (
    echo [ERROR] GEMINI_API_KEY not set
    echo.
    echo Set it in .env or run:
    echo set GEMINI_API_KEY=your_key_here
    pause
    exit /b 1
)

REM Install dependencies
echo [1/3] Installing Python dependencies...
pip install google-generativeai --quiet

REM Check if documind service exists
if not exist "deuxieme_cerveau\services\documind_service.py" (
    echo [WARNING] documind_service.py not found
    echo Run integration script first
    pause
)

REM Start Flask with Documind
echo [2/3] Starting Flask server...
cd deuxieme_cerveau
start "Flask-Documind" python app.py

REM Wait for server
timeout /t 3 /nobreak >nul

REM Open browser
echo [3/3] Opening browser...
start http://127.0.0.1:5008/documind

echo.
echo ========================================
echo Documind RAG is running!
echo ========================================
echo.
echo Access: http://127.0.0.1:5008/documind
echo Stop: Close Flask-Documind window
echo.
pause
