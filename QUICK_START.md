# Quick Start Guide - Dashboard

## One-Click Start (Easiest Method)

### Windows:
Double-click **`start_dashboard.bat`** in the root folder.

This will:
1. Start the Node.js backend (port 5001)
2. Start the Python ML service (port 5002)
3. Open your browser to the dashboard

### Alternative (PowerShell):
Right-click **`start_dashboard.ps1`** → "Run with PowerShell"

---

## Manual Start (Step-by-Step)

### Prerequisites Check:
- ✅ MongoDB is running
- ✅ Node.js is installed
- ✅ Python virtual environment is set up

### Step 1: Start MongoDB
Make sure MongoDB is running on your system.

**Windows (if installed as service):**
- MongoDB should auto-start
- Or start manually: `mongod`

**Check if running:**
```powershell
# Should show mongod.exe process
Get-Process mongod
```

### Step 2: Start Node.js Backend

Open a terminal in the project root:
```powershell
cd backend
npm start
```

You should see:
```
Server running on port 5001
MongoDB connected
```

**Keep this terminal open!**

### Step 3: Start Python ML Service

Open a **NEW** terminal in the project root:
```powershell
cd Sign-Language
.\venv\Scripts\python.exe ml_prediction_service.py
```

You should see:
```
ML model loaded successfully
Running on http://0.0.0.0:5002
```

**Keep this terminal open!**

### Step 4: Open Dashboard

Open your browser and go to:
```
http://localhost:5001
```

---

## What You'll See

1. **Login/Signup Page** - Create an account or log in
2. **Dashboard Home** - View statistics and quick actions
3. **Sign Detection** - Real-time camera-based sign language detection
4. **History** - View all your predictions

---

## Troubleshooting

### "Cannot connect to backend"
- Check if Node.js backend is running on port 5001
- Check terminal for errors
- Try: `http://localhost:5001/api/auth/health` (if you add this endpoint)

### "Prediction service unavailable"
- Check if Python ML service is running on port 5002
- Make sure `cnn8grps_rad1_model.h5` exists in `Sign-Language/` folder
- Check Python terminal for errors

### "MongoDB connection error"
- Make sure MongoDB is running
- Check `backend/.env` file has correct `MONGODB_URI`
- Default: `mongodb://localhost:27017/sign-language-app`

### "Module not found" errors
- For Python: Make sure venv is activated and packages installed
- For Node.js: Run `npm install` in `backend/` folder

### Port already in use
- Change ports in:
  - `backend/app.js` (PORT variable)
  - `Sign-Language/ml_prediction_service.py` (port variable)
  - Update `backend/app.js` ML_SERVICE_URL accordingly

---

## Stopping the Servers

1. Close the terminal windows (Backend and ML Service)
2. Or press `Ctrl+C` in each terminal

---

## Next Steps After Starting

1. **Create Account**: Sign up with email and password
2. **Login**: Use your credentials
3. **Test Detection**: 
   - Go to "Sign Detection" in sidebar
   - Click "Start Camera"
   - Show sign language gestures
4. **View History**: Check "History" to see all predictions

---

## Development Mode

### Backend (with auto-reload):
```powershell
cd backend
npm run dev
```

### Python ML Service (with debug):
Already runs in debug mode by default.

---

## File Structure

```
SGP/
├── start_dashboard.bat      ← Double-click this!
├── start_dashboard.ps1      ← Or this (PowerShell)
├── backend/                  ← Node.js server
│   └── app.js
├── Sign-Language/           ← Python ML service
│   ├── ml_prediction_service.py
│   └── cnn8grps_rad1_model.h5
├── dashboard.html           ← Main dashboard
├── app.js                   ← Frontend JavaScript
└── styles.css               ← Dashboard styles
```

---

## Need Help?

1. Check terminal output for error messages
2. Verify all services are running:
   - Backend: http://localhost:5001
   - ML Service: http://localhost:5002/health
3. Check browser console (F12) for frontend errors

