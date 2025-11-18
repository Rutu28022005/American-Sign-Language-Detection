# Quick Setup Guide

## Step-by-Step Setup

### 1. Start MongoDB
Make sure MongoDB is running on your system:
```bash
# Windows (if installed as service, it should auto-start)
# Or start manually:
mongod

# Linux/Mac
sudo systemctl start mongodb
# or
mongod
```

### 2. Start Backend (Node.js)

Open a terminal:
```bash
cd backend
npm install
npm start
```

You should see: `Server running on port 5001`

### 3. Start ML Service (Python)

Open another terminal:
```bash
cd Sign-Language

# Create and activate virtual environment (if not done)
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r ml_requirements.txt

# Start service
python ml_prediction_service.py
```

You should see: `ML model loaded successfully` and `Running on http://0.0.0.0:5002`

### 4. Access Dashboard

Open your browser and go to:
```
http://localhost:5001
```

## Verification Checklist

- [ ] MongoDB is running
- [ ] Backend (Node.js) is running on port 5001
- [ ] ML service (Python) is running on port 5002
- [ ] Can access http://localhost:5001 in browser
- [ ] Can see login/signup page
- [ ] Can create account and login
- [ ] Can access dashboard after login
- [ ] Camera permissions work (for detection)

## Common Issues

**Port already in use:**
- Change PORT in backend/.env or kill the process using the port

**MongoDB connection error:**
- Check if MongoDB is running
- Verify MONGODB_URI in backend/.env

**ML model not found:**
- Ensure `cnn8grps_rad1_model.h5` is in Sign-Language/ directory
- Check file permissions

**Camera not working:**
- Grant browser permissions
- Check if camera is being used by another app
- Try different browser

## Next Steps

1. Create your account
2. Test sign detection
3. View prediction history
4. Explore the dashboard features

