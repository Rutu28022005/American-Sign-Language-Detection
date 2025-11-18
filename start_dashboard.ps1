# PowerShell script to start the Sign Language Detection Dashboard
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting Sign Language Detection Dashboard" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if MongoDB is running (optional)
Write-Host "[1/4] Checking MongoDB..." -ForegroundColor Yellow
# Add MongoDB check if needed

# Start Node.js Backend
Write-Host "[2/4] Starting Node.js Backend (Port 5001)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; npm start"
Start-Sleep -Seconds 3

# Start Python ML Service
Write-Host "[3/4] Starting Python ML Service (Port 5002)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd Sign-Language; if (Test-Path '.\venv\Scripts\python.exe') { .\venv\Scripts\python.exe ml_prediction_service.py } else { Write-Host 'ERROR: Virtual environment not found!' -ForegroundColor Red; pause }"
Start-Sleep -Seconds 3

# Open browser
Write-Host "[4/4] Opening Dashboard in browser..." -ForegroundColor Yellow
Start-Sleep -Seconds 5
Start-Process "http://localhost:5001"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Dashboard started!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Backend: http://localhost:5001" -ForegroundColor Cyan
Write-Host "ML Service: http://localhost:5002" -ForegroundColor Cyan
Write-Host ""
Write-Host "Two new windows have opened:" -ForegroundColor Yellow
Write-Host "  - Backend Server (Node.js)" -ForegroundColor White
Write-Host "  - ML Service (Python)" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to exit (servers will continue running)..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

