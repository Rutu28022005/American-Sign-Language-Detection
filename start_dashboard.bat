@echo off
echo ========================================
echo Starting Sign Language Detection Dashboard
echo ========================================
echo.

REM Ensure we run from this script folder
cd /d "%~dp0"

REM Activate venv (works if venv exists in project root)
if exist ".\venv\Scripts\activate.bat" (
    call ".\venv\Scripts\activate.bat"
) else (
    echo WARNING: venv not found at .\venv. Make sure you activate your venv manually.
)

REM Start Flask server to serve front.html and static files
echo [1/3] Starting local server (launch_server.py)...
start "Launch Server" cmd /k "%~dp0\venv\Scripts\python.exe" "%~dp0\launch_server.py"

REM give server a moment to start
timeout /t 2 /nobreak >nul

REM Open dashboard in default browser
echo [2/3] Opening dashboard...
start http://127.0.0.1:5000

REM (Optional) start final_pred.py directly in new console (uncomment if you want it auto-started)
REM echo [3/3] Starting final_pred.py in new console...
REM start "Final Pred" cmd /k "%~dp0\venv\Scripts\python.exe" "%~dp0\final_pred.py"

echo.
echo ========================================
echo Dashboard started (or launching). Visit http://127.0.0.1:5000
echo ========================================
pause
