# Commands to Run the Dashboard

## Quick Start (Easiest)
**Double-click:** `start_dashboard.bat`

---

## Manual Commands (3 Terminals)

### Terminal 1: Start Node.js Backend
```powershell
cd C:\Users\Admin\Desktop\SGP\backend
npm start
```
**Expected output:**
```
Server running on port 5001
MongoDB connected
```

### Terminal 2: Start Python ML Service
```powershell
cd C:\Users\Admin\Desktop\SGP\Sign-Language
.\venv\Scripts\python.exe ml_prediction_service.py
```
**Expected output:**
```
ML model loaded successfully
Running on http://0.0.0.0:5002
```

### Terminal 3: (Optional) Check MongoDB
```powershell
# Check if MongoDB is running
Get-Process mongod
```

---

## Open Dashboard
Open your browser and go to:
```
http://localhost:5001
```

---

## Quick Commands Summary

### Start Everything (One Line Each)
```powershell
# Terminal 1 - Backend
cd backend && npm start

# Terminal 2 - ML Service  
cd Sign-Language && .\venv\Scripts\python.exe ml_prediction_service.py
```

### Stop Everything
- Press `Ctrl+C` in each terminal
- Or close the terminal windows

---

## Troubleshooting

### If backend fails:
```powershell
cd backend
npm install
npm start
```

### If Python ML service fails:
```powershell
cd Sign-Language
.\venv\Scripts\python.exe -m pip install -r ml_requirements.txt
.\venv\Scripts\python.exe ml_prediction_service.py
```

### Check if services are running:
```powershell
# Check Node.js (port 5001)
netstat -ano | findstr :5001

# Check Python (port 5002)
netstat -ano | findstr :5002
```

---

## What to Do After Starting

1. Open browser: `http://localhost:5001`
2. Sign up or login
3. Click "Sign Detection" → "Launch Detection App"
4. The `final_pred.py` window will open automatically!


